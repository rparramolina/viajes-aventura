import re
from config.settings import DB_ENGINE

def query_compat(sql):
    """
    Translates a SQL query from PostgreSQL syntax to SQL Server syntax if needed.
    """
    from config.settings import DB_ENGINE
    
    if DB_ENGINE == "oracle":
        # Oracle uses :1, :2, etc. for positional arguments
        parts = sql.split('%s')
        if len(parts) > 1:
            new_sql = ""
            for i, part in enumerate(parts[:-1]):
                new_sql += f"{part}:{i+1}"
            new_sql += parts[-1]
            return new_sql
        return sql
    
    if DB_ENGINE != "sqlserver":
        return sql

    # 1. Change %s to ? (SQL Server uses ? for placeholders in pyodbc)
    new_sql = sql.replace("%s", "?")

    # 2. Handle RETURNING id
    # Postgres: INSERT INTO ... VALUES (...) RETURNING id
    # SQL Server: INSERT INTO ... OUTPUT Inserted.id VALUES (...)
    
    returning_match = re.search(r"RETURNING\s+(\w+)", new_sql, re.IGNORECASE)
    if returning_match:
        col_name = returning_match.group(1)
        # Find the keyword VALUES or SELECT to insert OUTPUT before it
        # Handle cases with and without column lists
        match_vals = re.search(r"\b(VALUES|SELECT)\b", new_sql, re.IGNORECASE)
        if match_vals:
            idx = match_vals.start()
            insert_part = new_sql[:idx]
            values_part = new_sql[idx:]
            
            output_clause = f" OUTPUT Inserted.{col_name} "
            # Ensure we don't have multiple spaces
            new_sql = f"{insert_part.rstrip()}{output_clause}{values_part.lstrip()}"
            # Remove the original RETURNING part
            new_sql = re.sub(r"RETURNING\s+\w+", "", new_sql, flags=re.IGNORECASE)

    return new_sql.strip()
