import sqlite3
from config.constants import Constants

class DB(object):
    """DB initializes and manipulates SQLite3 databases."""

    def __init__(self, database=Constants.PROJECT_DIR+'\\files\\testdb.db', statements=[]):
        """Initialize a new or connect to an existing database.

        Accept setup statements to be executed.
        """

        #the database filename
        self.database = database
        #holds incomplete statements
        self.statement = ''
        #indicates if selected data is to be returned or printed
        self.display = False

        self.connect()

        #execute setup satements
        self.execute(statements)

        self.close()            

    def connect(self):
        """Connect to the SQLite3 database."""

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connected = True
        self.statement = ''

    def close(self): 
        """Close the SQLite3 database."""

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
        if sqlite3.complete_statement(self.statement):
            #the statement is not incomplete, it's complete
            return False
        else:
            #the statement is incomplete
            return True

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
            if self.incomplete(statement):
                #the statement is incomplete
                continue
            #the statement is complete
            try:
                statement = self.statement.strip()
                #reset the test statement
                self.statement = ''
                self.cursor.execute(statement)
                #retrieve selected data
                data = self.cursor.fetchall()
                if statement.upper().startswith('SELECT'):
                    #append query results
                    queries = data
                if statement.upper().startswith('INSERT'):
                    queries = self.cursor.lastrowid

            except sqlite3.Error as error:
                print('An error occurred:', error.args[0])
                print('For the statement:', statement)

        #only close the connection if opened in this function
        if close:
            self.close()

        return queries
