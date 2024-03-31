"""
Database-related functions
"""

from typing import Any

from sqlalchemy import text, create_engine, exc, CursorResult, Engine, Sequence


class Database:
    """
    Database class
    """
    def __init__(self) -> None:
        """
        Initialize Database object
        """
        self.url = 'mssql+pyodbc://DESKTOP-PGP19NP/data_site?driver=ODBC Driver 17 for SQL Server'

    def create_engine(self) -> Engine:
        """
        Create database engine
        """
        engine = create_engine(self.url, fast_executemany=True)
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

    def exec_select(self, sql_statement: str) -> list | None:
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

    # def execute_sql_file(self, sql_file_name: str, sql_type: str) -> list | None:
    #     """
    #     Read and execute a sql file
    #     """
    #     if sql_type == 'with_commit':
    #         sql_path = self.with_commit_folder + '/' + sql_file_name
    #         sql_command = utils.read_sql_file(sql_path)
    #         self.exec_statement(sql_command)
    #         return None
    #     if sql_type == 'without_commit':
    #         sql_path = self.without_commit_folder + '/' + sql_file_name
    #         sql_command = utils.read_sql_file(sql_path)
    #         return self.exec_select(sql_command)
    #     return None

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
