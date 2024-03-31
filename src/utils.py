


def read_sql_file(sql_path: str) -> str:
    """
    Read sql file from disk
    """
    with open(sql_path, 'r') as file:
        sql_contents = file.read()
    return sql_contents
