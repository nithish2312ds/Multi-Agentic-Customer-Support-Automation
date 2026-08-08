import sqlite3

DB = 'memory.db'


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS conversations (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        query       TEXT,
        response    TEXT
    )''')
    conn.commit()
    conn.close()


def save_memory(state):
    if state.get("issue_type") == "Memory":
        return state

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO conversations (customer_id, query, response) VALUES (?, ?, ?)',
        (state['customer_id'], state['query'], state['final_response'])
    )
    conn.commit()
    conn.close()
    return state


def recall_previous_issue(customer_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        'SELECT query FROM conversations WHERE customer_id = ? ORDER BY id DESC LIMIT 1',
        (customer_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None