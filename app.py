from flask import Flask, request, jsonify
import mysql.connector
import redis
import os
import json

app = Flask(__name__)

def db_conn():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

cache = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return "Log Monitoring API Running"

@app.route("/log", methods=["POST"])
def add_log():
    data = request.json

    service = data["service"]
    level = data["level"]
    message = data["message"]

    conn = db_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO logs(service, level, message) VALUES(%s,%s,%s)",
        (service, level, message)
    )

    conn.commit()

    log_entry = {
        "service": service,
        "level": level,
        "message": message
    }

    cache.lpush("recent_logs", json.dumps(log_entry))
    cache.ltrim("recent_logs", 0, 20)

    cur.close()
    conn.close()

    return jsonify({"status": "log stored"})

@app.route("/logs")
def get_logs():
    conn = db_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)

@app.route("/recent")
def recent_logs():
    logs = cache.lrange("recent_logs", 0, 20)
    return jsonify(logs)

@app.route("/dashboard")
def dashboard():
    conn = db_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM logs WHERE level='ERROR'")
    errors = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM logs")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "total_logs": total,
        "error_logs": errors
    })

app.run(host="0.0.0.0", port=5000)
