from flask import Flask, jsonify
import os

app = Flask(__name__)
db_host = os.getenv('DB_HOST', 'localhost')

@app.route("/")
def home():
    return jsonify({"service": "API", "status": "running", "db": db_host})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/data")
def data():
    return jsonify({"data": "Sample data from API", "source": "database"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
