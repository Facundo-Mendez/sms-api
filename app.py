from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sms_database"]
collection = db["sms_messages"]

@app.route("/api/sms", methods=["POST"])
def receive_sms():
    data = request.json
    sender = data.get("sender")
    message = data.get("message")
    time = data.get("time")

    # Guardar en la base de datos
    sms_data = {"sender": sender, "message": message, "time": time}
    collection.insert_one(sms_data)

    return jsonify({"status": "success", "message": "SMS received"}), 200

if __name__ == "__main__":
    app.run(debug=True)
