#!/usr/bin/env python

import os
import psycopg2
import psycopg2.extras
import psycopg2.errors
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT users.id_users, users.screen_name
            FROM users
            JOIN credentials ON users.id_users = credentials.id_users
            WHERE users.screen_name = %s
            AND credentials.password_hash = %s
        """, (username, password_hash))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["id_users"] = user["id_users"]
            session["screen_name"] = user["screen_name"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html", error=None)


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            return render_template("create_account.html", error="Passwords do not match")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (screen_name) VALUES (%s) RETURNING id_users;",
                (username,)
            )
            user_id = cur.fetchone()["id_users"]
            cur.execute(
                "INSERT INTO credentials (id_users, password_hash) VALUES (%s, %s);",
                (user_id, password_hash)
            )
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return render_template("create_account.html", error="Username already exists")
        finally:
            cur.close()
            conn.close()

        session["id_users"] = user_id
        session["screen_name"] = username
        return redirect(url_for("index"))

    return render_template("create_account.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    if not session.get("id_users"):
        return redirect(url_for("login"))

    if request.method == "POST":
        text = request.form["text"]
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tweets (id_users, text) VALUES (%s, %s);",
            (session["id_users"], text)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    return render_template("create_message.html", error=None)