#!/usr/bin/env python3
import os
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import random

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://twitter:twitter@localhost:5433/twitter_dev")

WORDS = [
    "python", "flask", "docker", "postgres", "sql", "index", "query",
    "database", "twitter", "clone", "flask", "learning", "coding",
    "coffee", "linux", "github", "commit", "deploy", "server", "cloud",
    "data", "science", "machine", "learning", "neural", "network",
    "algorithm", "recursion", "function", "variable", "loop", "debug",
]

def random_tweet():
    length = random.randint(5, 15)
    return " ".join(random.choices(WORDS, k=length))

def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    NUM_USERS = 1_000_000
    NUM_TWEETS = 1_000_000
    BATCH_SIZE = 10_000

    print("Inserting users...")
    for batch_start in range(0, NUM_USERS, BATCH_SIZE):
        batch = [
            (f"user_{batch_start + i}",)
            for i in range(BATCH_SIZE)
            if batch_start + i < NUM_USERS
        ]
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO users (screen_name) VALUES %s ON CONFLICT DO NOTHING;",
            batch
        )
        conn.commit()
        print(f"  users: {batch_start + len(batch)}/{NUM_USERS}")

    print("Fetching user IDs...")
    cur.execute("SELECT id_users FROM users;")
    user_ids = [row[0] for row in cur.fetchall()]

    print("Inserting tweets...")
    base_time = datetime(2020, 1, 1)
    for batch_start in range(0, NUM_TWEETS, BATCH_SIZE):
        batch = [
            (
                random.choice(user_ids),
                random_tweet(),
                base_time + timedelta(minutes=batch_start + i)
            )
            for i in range(BATCH_SIZE)
            if batch_start + i < NUM_TWEETS
        ]
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO tweets (id_users, text, created_at) VALUES %s;",
            batch
        )
        conn.commit()
        print(f"  tweets: {batch_start + len(batch)}/{NUM_TWEETS}")

    cur.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
