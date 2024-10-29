CREATE TABLE IF NOT EXISTS notes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id));