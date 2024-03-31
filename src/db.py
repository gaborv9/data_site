"""
Database-related functions
"""

from typing import Any

from sqlalchemy import text, create_engine, exc, CursorResult, Engine, Sequence

import utils

class Database:
    """
    Database class
    """
    def __init__(self, root_folder, with_commit_folder, without_commit_folder) -> None:
        """
        Intialize Database object
        """
        self.root_folder = root_folder
        self.with_commit_folder = with_commit_folder
        self.without_commit_folder = without_commit_folder

    def create_engine(self) -> Engine:
        """
        Create database engine
        """
        engine = create_engine('mssql+pyodbc://DESKTOP-PGP19NP/data_site?driver=ODBC Driver 17 for SQL Server',
                               fast_executemany=True)
        return engine

    def exec_statement(self, sql_statement: str) -> CursorResult[Any] | None:
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
            return None

    def exec_select(self, sql_statement: str) -> Sequence | None:
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
            return None

    def execute_sql_file(self, sql_file_name: str, sql_type: str) -> Sequence | None:
        """
        Read and execute a sql file
        """
        if sql_type == 'with_commit':
            sql_path = self.with_commit_folder + '/' + sql_file_name
            sql_command = utils.read_sql_file(sql_path)
            self.exec_statement(sql_command)
            return None
        if sql_type == 'without_commit':
            sql_path = self.without_commit_folder + '/' + sql_file_name
            sql_command = utils.read_sql_file(sql_path)
            return self.exec_select(sql_command)
        return None

    def execute_sql_command(self, sql_command, command_type: str) -> Sequence | None:
        """
        Execute sql command
        """
        if command_type == 'with_commit':
            self.exec_statement(sql_command)
            return None
        if command_type == 'without_commit':
            return self.exec_select(sql_command)
        return None
