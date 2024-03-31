from typing import Any

from sqlalchemy import text, create_engine, exc, CursorResult

import utils

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
        """
        Execute sql files that need a database commit
        """
        try:
            engine = self.create_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql_statement))
                conn.commit()
            return result
        except exc.SQLAlchemyError as e:
            print(e)

    def exec_select(self, sql_statement: str):
        """
        Execute sql files that do not need a database commit
        """
        try:
            engine = self.create_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql_statement)).fetchall()
            return result
        except exc.SQLAlchemyError as e:
            print(e)

    def execute_sql_file(self, sql_file_name: str, type: str):
        """
        Read and execute a sql file
        """
        if type == 'with_commit':
            sql_path = self.with_commit_folder + '/' + sql_file_name
            sql_command = utils.read_sql_file(sql_path)
            self.exec_statement(sql_command)
        elif type == 'without_commit':
            sql_path = self.without_commit_folder + '/' + sql_file_name
            sql_command = utils.read_sql_file(sql_path)
            return self.exec_select(sql_command)

    def execute_sql_command(self, sql_command, type: str):
        """
        Execute sql command
        """
        if type == 'with_commit':
            self.exec_statement(sql_command)
        elif type == 'without_commit':
            return self.exec_select(sql_command)







