import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract and log the query
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            # Find SQL query in arguments
            for arg in args:
                if isinstance(arg, str) and any(keyword in arg.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                    query = arg
                    break
        
        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    
    return wrapper
