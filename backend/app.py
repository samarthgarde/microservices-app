import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection details (match with your docker run command)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "projectdb"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "secret"),
    "host": os.getenv("DB_HOST", "localhost"),  # default local
    "port": int(os.getenv("DB_PORT", 5432))
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            text VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/message', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = [row[0] for row in rows]
    return jsonify({"messages": messages})

@app.route('/api/add', methods=['POST'])
def add_message():
    data = request.json
    message = data.get("message", "")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (text) VALUES (%s);", (message,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success", "message": message})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
