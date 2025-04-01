import sqlite3
import pandas as pd

# Initialize the database and create tables
def initialize_db():
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()

    # Create the FAQ table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    ''')

    # Import CSV data into the database
    data = pd.read_csv('data/faq_data.csv')
    for _, row in data.iterrows():
        cursor.execute('INSERT INTO faq (question, answer) VALUES (?, ?)', (row['question'], row['answer']))

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Run the initialization script
if __name__ == "__main__":
    initialize_db()
