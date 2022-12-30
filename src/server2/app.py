from flask import Flask, request
import json
import os
import platform
import shutil
import psutil

app = Flask(__name__)

status = True

@app.route("/ping", methods=["GET"])
def set_rpc_status():
    return {"status": status}

@app.route("/data", methods=["POST"])
def data_endpoint():
    data = request.json

    try:
        with open("storage.json", "r") as f:
            current_data = json.load(f)
    except:
        current_data = data
    
    current_data.update(data)
    with open("storage.json", "w") as f:
        json.dump(current_data, f)

    return {"transfer": True}

@app.route("/retrieve", methods=["POST"])
def retrieve_data():
    pubkey = request.json["pubkey"]

    with open("storage.json", "r") as f:
        data = json.load(f)
    pubkey_data = data[pubkey]
    return {"data": pubkey_data}

@app.route("/performance", methods=["GET"])
def performance_endpoint():
    stored_data_size = os.stat("storage.json")[6]
    a, b, free_storage = shutil.disk_usage("/")
    architecture = platform.machine()
    processor = platform.processor()
    ram = f"{round(psutil.virtual_memory().total/(1024**3))} GB"
    return {"architecture": architecture, 
            "processor": processor, 
            "ram": ram,
            "free_storage": free_storage,
            "used_storage": f"{stored_data_size/(1024**3)} GB"}


    

if __name__ == "__main__":
    app.run(host="localhost", port=6000, debug=True)