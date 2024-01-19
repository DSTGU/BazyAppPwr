import psycopg2
from psycopg2 import sql

class PostgreSQLConnection:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def create_connection(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            print("Connection established.")
        except psycopg2.Error as e:
            print(f"Error: Unable to connect to the database. {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query, params=None, fetch_result=True):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")

            if fetch_result:
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()
                return columns, result
        except psycopg2.Error as e:
            print(f"Error: Unable to execute the query. {e}")
        finally:
            cursor.close()

    def execute_call(self, call):
        cursor = self.connection.cursor()
        try:
            cursor.execute(call)
            self.connection.commit()
            print("Call executed successfully.")

        except psycopg2.Error as e:
            print(f"Error: Unable to execute the call. {e}")
        finally:
            cursor.close()