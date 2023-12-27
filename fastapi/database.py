import pyodbc


class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None

    def connect(self):
        print("Connecting to database...")
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        print("Disconnecting from database...")
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def query(self, sql_query):
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def schema(self):
        table_names = [
            row[0]
            for row in self.query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;")
        ]

        definitions = []
        for table_name in table_names:
            # cursor.execute(get_def_stmt, (table_name,))
            # rows = cursor.fetchall()
            rows = self.query(
                f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
            )

            create_table_stmt = f"CREATE TABLE {table_name} (\n"
            for row in rows:
                create_table_stmt += f"{row[0]} {row[1]},\n"
            create_table_stmt = create_table_stmt.rstrip(",\n") + "\n);"

            definitions.append(create_table_stmt)

        table_definitions = "\n\n".join(definitions)

        return table_definitions
