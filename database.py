import sqlite3


DB_NAME = "anonymous_messages.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            username TEXT,
            first_name TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_message(
    sender_id,
    receiver_id,
    username,
    first_name,
    message
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (
            sender_id,
            receiver_id,
            username,
            first_name,
            message
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        sender_id,
        receiver_id,
        username,
        first_name,
        message
    ))

    connection.commit()
    connection.close()
