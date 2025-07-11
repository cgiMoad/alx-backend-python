import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # Return query results on enter

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Usage example:
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as users_over_25:
    print(users_over_25)
