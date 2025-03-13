from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

# URI de conexión a MongoDB Atlas
uri = "mongodb+srv://dbPines:Mausof1515@cluster0.lncbj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Crear un cliente de MongoDB y conectar al servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Enviar un ping para confirmar una conexión exitosa
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Conectar a la base de datos y colección específicas
db = client["sms_database"]
collection = db["sms_messages"]

@app.route("/api/sms", methods=["POST"])
def receive_sms():
    data = request.json
    sender = data.get("sender")
    message = data.get("message")
    time = data.get("time")
    
    # Si el mensaje tiene un PIN, extraerlo
    pin = None
    if "PIN" in message:  # Suponiendo que el mensaje tiene un formato como "PIN: 1234"
        pin = message.split("PIN:")[1].strip()

    # Guardar en la base de datos
    sms_data = {"sender": sender, "message": message, "time": time, "pin": pin}
    collection.insert_one(sms_data)

    return jsonify({"status": "success", "message": "SMS received"}), 200


@app.route("/api/sms", methods=["GET"])
def get_sms():
    # Obtener los mensajes de la base de datos
    messages = collection.find()
    sms_list = [{"sender": sms["sender"], "message": sms["message"], "time": sms["time"], "pin": sms.get("pin")} for sms in messages]

    return jsonify({"status": "success", "messages": sms_list}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
