-- Starter SQLite-compatible schema; not yet connected to application code.
-- Do not commit real conversation data or secrets.

CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY,
    preference_key TEXT NOT NULL UNIQUE,
    preference_value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    id INTEGER PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    message_text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_conversation_messages_conversation_id
    ON conversation_messages (conversation_id);
