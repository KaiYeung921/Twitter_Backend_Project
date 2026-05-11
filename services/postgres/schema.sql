CREATE TABLE users(
    id_users BIGSERIAL primary key,
    screen_name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE tweets(
    id_tweets BIGSERIAL primary key,
    id_users BIGINT NOT NULL references users(id_users),
    created_at TIMESTAMPTZ DEFAULT now(),
    text TEXT not null,
    text_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', text)) STORED

);

CREATE TABLE credentials(
    id_users BIGINT PRIMARY KEY REFERENCES users(id_users),
    password_hash TEXT NOT NULL
);

CREATE INDEX idx_tweets_created_at ON tweets(created_at DESC);
CREATE INDEX idx_tweets_id_users ON tweets(id_users);

CREATE EXTENSION IF NOT EXISTS rum;
CREATE INDEX idx_tweets_rum ON tweets USING rum(text_tsv);



 