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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waiting_users (
            user_id INTEGER PRIMARY KEY,
            receiver_id INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waiting_replies (
            user_id INTEGER PRIMARY KEY,
            message_id INTEGER NOT NULL
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

    message_id = cursor.lastrowid

    connection.close()

    return message_id


def get_message(message_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sender_id,
            receiver_id
        FROM messages
        WHERE id = ?
    """, (message_id,))

    result = cursor.fetchone()

    connection.close()

    return result


def get_received_messages(receiver_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            message,
            created_at
        FROM messages
        WHERE receiver_id = ?
        ORDER BY id DESC
    """, (receiver_id,))

    results = cursor.fetchall()

    connection.close()

    return results


def save_waiting_user(user_id, receiver_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO waiting_users (
            user_id,
            receiver_id
        )
        VALUES (?, ?)
    """, (
        user_id,
        receiver_id
    ))

    connection.commit()
    connection.close()


def get_waiting_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT receiver_id
        FROM waiting_users
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def delete_waiting_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM waiting_users
        WHERE user_id = ?
    """, (user_id,))

    connection.commit()
    connection.close()


def save_waiting_reply(user_id, message_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO waiting_replies (
            user_id,
            message_id
        )
        VALUES (?, ?)
    """, (
        user_id,
        message_id
    ))

    connection.commit()
    connection.close()


def get_waiting_reply(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT message_id
        FROM waiting_replies
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def delete_waiting_reply(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM waiting_replies
        WHERE user_id = ?
    """, (user_id,))

    connection.commit()
    connection.close()
