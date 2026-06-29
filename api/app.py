from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"service": "API", "status": "running", "db": "connected"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/data")
def data():
    return jsonify({"data": "Sample data from API", "source": "database"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)