CREATE TABLE users (
  id INTEGER PRIMARY KEY NOT NULL,
  user_id INTEGER NOT NULL UNIQUE,
  is_active INTEGER NOT NULL DEFAULT 1
);