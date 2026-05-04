#!/usr/bin/env python3
import os
import hashlib
import psycopg2
from datetime import datetime, timedelta
import random

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://twitter:twitter@localhost:5432/twitter_dev")

USERS = [
    "alice", "bob", "carol", "dave", "eve",
    "frank", "grace", "heidi", "ivan", "judy",
]

TWEET_TEMPLATES = [
    "Hello world! This is my first tweet.",
    "Just had the best coffee ever.",
    "Python is a great programming language.",
    "Docker makes deployment so much easier.",
    "Learning SQL is actually pretty fun.",
    "Finished my homework, time to relax.",
    "The weather is nice today.",
    "Can't believe how fast time flies.",
    "Working on a Twitter clone for class.",
    "Postgres full text search is powerful.",
    "Another day, another commit.",
    "Indexes make queries so much faster.",
    "Flask is a lightweight web framework.",
    "I love open source software.",
    "Just pushed to GitHub, CI is green!",
]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("DELETE FROM tweets;")
    cur.execute("DELETE FROM credentials;")
    cur.execute("DELETE FROM users;")

    user_ids = []
    for username in USERS:
        cur.execute(
            "INSERT INTO users (screen_name) VALUES (%s) RETURNING id_users;",
            (username,)
        )
        user_id = cur.fetchone()[0]
        user_ids.append(user_id)
        cur.execute(
            "INSERT INTO credentials (id_users, password) VALUES (%s, %s);",
            (user_id, hash_password("password123"))
        )

    base_time = datetime.now() - timedelta(days=30)
    for i in range(100):
        user_id = random.choice(user_ids)
        text = random.choice(TWEET_TEMPLATES) + f" (#{i})"
        created_at = base_time + timedelta(minutes=i * 30)
        cur.execute(
            "INSERT INTO tweets (id_users, text, created_at) VALUES (%s, %s, %s);",
            (user_id, text, created_at)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Done: 10 users, 100 tweets inserted.")

if __name__ == "__main__":
    main()
