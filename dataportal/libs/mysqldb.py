import mysql.connector
# from flask import Flask
from config.constants import Constants

# app = Flask(__name__)

class DB(object):
    cursor = None
    connected = False
    statement = None

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=Constants.DB_HOST,
            user=Constants.DB_USER,
            passwd=Constants.DB_PASSWORD,
            database=Constants.DB_NAME
        )

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
            print ('An error has occurerd: ' +
                'You may only execute one statement at a time.')
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
            except :
                print('An error occurred:')
                print('For the statement:', statement)

        #only close the connection if opened in this function
        if close:
            self.close()

        return queries
