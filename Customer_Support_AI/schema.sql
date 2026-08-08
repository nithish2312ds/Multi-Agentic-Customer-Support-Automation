CREATE TABLE IF NOT EXISTS conversations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    query       TEXT,
    response    TEXT
);