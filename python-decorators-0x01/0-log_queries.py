import sqlite3
import functools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#### decorator to log SQL queries

def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.
    
    This decorator wraps functions that execute database queries and logs
    the SQL query string before the function executes.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        # Check if 'query' is in kwargs
        if 'query' in kwargs:
            query = kwargs['query']
        # Check if there are positional arguments and assume first one might be query
        elif args:
            # Look for string arguments that might be SQL queries
            for arg in args:
                if isinstance(arg, str) and any(keyword in arg.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP']):
                    query = arg
                    break
            else:
                query = "Query not found in arguments"
        else:
            query = "No query provided"
        
        # Log the query
        logging.info(f"Executing SQL Query: {query}")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Additional example functions to demonstrate the decorator
@log_queries
def insert_user(query, user_data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query, user_data)
    conn.commit()
    conn.close()
    return cursor.lastrowid

@log_queries
def update_user_email(query, email, user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query, (email, user_id))
    conn.commit()
    conn.close()
    return cursor.rowcount

# Example usage
if __name__ == "__main__":
    # Create a sample database and table for testing
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Jane Smith", "jane@example.com"))
    conn.commit()
    conn.close()
    
    #### fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users")
    
    # Test other functions
    insert_user("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob Wilson", "bob@example.com"))
    update_user_email("UPDATE users SET email = ? WHERE id = ?", "newemail@example.com", 1)
