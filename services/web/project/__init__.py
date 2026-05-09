#!/usr/bin/env python

import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * 20
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT tweets.text, tweets.created_at, users.screen_name
        FROM tweets
        JOIN users ON tweets.id_users = users.id_users
        ORDER BY tweets.created_at DESC
        LIMIT 20 OFFSET %s
    """, (offset,))
    tweets = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tweets=tweets, page=page)

@app.route("/search")
def serach():
    query = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * 20
    tweets = []
    if query:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                users.screen_name,
                tweets.created_at,
                ts_headline('english', tweets.text, to_tsquery('english', %s),
                    'HighlightAll=true, StartSel=<mark>, StopSel=</mark>') AS text,
                ts_rank(to_tsvector('english', tweets.text), to_tsquery('english', %s)) AS rank
            FROM tweets
            JOIN users ON tweets.id_users = users.id_users
            WHERE to_tsvector('english', tweets.text) @@ to_tsquery('english', %s)
            ORDER BY rank DESC
            LIMIT 20 OFFSET %s
        """, (query, query, query, offset))
        tweets = cur.fetchall()
        cur.close()
        conn.close()
    return render_template("search.html", tweets=tweets, query=query, page=page)
