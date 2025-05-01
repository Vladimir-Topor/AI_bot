import sqlite3


def create_database(db_name='chat_history.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Таблица со стилями общения
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        communication_style TEXT
    )
    ''')
    
    # Таблица историй общения
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message_text TEXT,
        is_user_message BOOLEAN,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close()


# Стиль общения
def communication_style(user_id: int, style: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, communication_style) VALUES (?, ?)', 
                  (user_id, style))
    conn.commit()
    conn.close()


# Сохраняет сообщения
def save_message(user_id: int, text: str, is_user_message: bool):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM messages WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]    
# очистка контекста ели сообщений много
    if count > 30:
        cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))

    cursor.execute('INSERT INTO messages (user_id, message_text, is_user_message) VALUES (?, ?, ?)', 
                  (user_id, text, is_user_message))

    conn.commit()
    conn.close()


# Очистка контекста
def clear_chat_history(user_id: int):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()