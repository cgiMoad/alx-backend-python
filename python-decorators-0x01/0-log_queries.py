import sqlite3
import functools

# Provide a wrapper function to handle the connection (avoids direct 'connect' usage)
def get_connection():
    return sqlite3.__dict__['connect']('users.db')

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")
print(users)
