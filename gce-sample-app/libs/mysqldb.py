import sqlalchemy
import os
import sys
from config.constants import Constants

class DB(object):
    cursor = None
    connected = False
    statement = None

    def __init__(self):
        if os.environ.get('GAE_ENV') == 'standard':
            connStr = "mysql://{}:{}@/{}?unix_socket=/cloudsql/{}".format(
                        Constants.DB_USER, 
                        Constants.DB_PASSWORD, 
                        Constants.DB_NAME, 
                        Constants.CONN_CLOUD)
        else:
            connStr = "mysql://{}:{}@{}/{}".format(
                        Constants.DB_USER, 
                        Constants.DB_PASSWORD, 
                        Constants.DB_HOST,
                        Constants.DB_NAME)

        self.connection = sqlalchemy.create_engine(
                            connStr,
                            pool_size=5,
                            max_overflow=2,
                            pool_timeout=30,  # 30 seconds
                            pool_recycle=1800,  # 30 minutes
                            ).raw_connection()

        # connect to database
        self.connect()

    def connect(self):
        """ Connect to database """
        self.cursor = self.connection.cursor()
        self.connected = True
        self.statement = ''

    def close(self): 
        """Close DB connection."""
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def incomplete(self, statement):
        """Concatenate clauses until a complete statement is made."""

        self.statement += statement
        if self.statement.count(';') > 1:
            print ('An error has occurerd: You may only execute one statement at a time.')
            print('For the statement: %s' % self.statement)
            self.statement = ''
        # if sqlite3.complete_statement(self.statement):
        #     #the statement is not incomplete, it's complete
        #     return False
        else:
            #the statement is incomplete
            return False

    def execute(self, statements):
        queries = []
        close = False
        if not self.connected:
            print("orj bn123")
            #open a previously closed connection
            self.connect()
            #mark the connection to be closed once complete
            close = True
        if type(statements) == str:
            #all statements must be in a list
            statements = [statements]
        for statement in statements:
            # the statement is incomplete
            if self.incomplete(statement):
                continue

            #the statement is complete
            try:
                statement = self.statement.strip()                
                #reset the test statement
                self.statement = ''           
                self.cursor.execute(statement)
                if statement.upper().startswith('SELECT'):
                    # retrieve selected data
                    data = self.cursor.fetchall()
                    
                    # append query results with named columns
                    columns = self.cursor.description
                    queries = [{columns[index][0]: column for index, column in enumerate(value)} for value in data]
                if statement.upper().startswith('INSERT'):
                    queries = self.cursor.lastrowid

                self.connection.commit()                
            except:
                e = sys.exc_info()[0]
                print('An error occurred:')
                print(e)
                return False

        #close db connection
        if close:
            self.close()

        return queries
