from typing import Any

from sqlalchemy import text, create_engine, exc, CursorResult


class Database:
    def __init__(self, root_folder, with_commit_folder, without_commit_folder):
        self.root_folder = root_folder
        self.with_commit_folder = with_commit_folder
        self.without_commit_folder = without_commit_folder

    def create_engine(self):
        engine = create_engine('mssql+pyodbc://DESKTOP-PGP19NP/data_site?driver=ODBC Driver 17 for SQL Server',
                               fast_executemany=True)
        return engine

    def exec_statement(self, sql_statement: str) -> CursorResult[Any]:
        try:
            engine = self.create_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql_statement))
                conn.commit()
            return result
        except exc.SQLAlchemyError as e:
            print(e)

    def exec_select(self, sql_statement: str):
        try:
            engine = self.create_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql_statement)).fetchall()
            return result
        except exc.SQLAlchemyError as e:
            print(e)

    def execute_sql(self, sql_file_name: str, type: str):
        if type == 'with_commit':
            sql_path = self.with_commit_folder + '/' + sql_file_name
            sql_command = read_sql_file(sql_path)
            self.exec_statement(sql_command)
        elif type == 'without_commit':
            sql_path = self.without_commit_folder + '/' + sql_file_name
            sql_command = read_sql_file(sql_path)
            return self.exec_select(sql_command)

    def load_data(self, table_name, data):
        engine = self.create_engine()
        data.to_sql(name=table_name, con=engine, if_exists='append', index=False)


def read_sql_file(sql_path: str) -> str:
    with open(sql_path, 'r') as file:
        sql_contents = file.read()
    return sql_contents


