from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Flask app is running"})

@app.route("/user/plans")
def get_plans():
    return jsonify({"success": True, "plans": [{"id": 1, "name": "Basic Plan", "price": 29.99}]})

@app.route("/user/cancel-plan", methods=["POST"])
def cancel_plan():
    data = request.get_json()
    user_id = data.get("user_id")
    return jsonify({"success": True, "message": f"Plan cancelled for user {user_id}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
