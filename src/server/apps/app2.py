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
        with open("data/storage1.json", "r") as f:
            current_data = json.load(f)
            current_data.update(data)
    except:
        current_data = data

    with open("data/storage2.json", "w") as f:
        json.dump(current_data, f)

    return {"transfer": True}

@app.route("/performance", methods=["GET"])
def performance_endpoint():
    stored_data_size = os.stat("data/storage2.json")[6]
    a, b, free_storage = shutil.disk_usage("/")
    architecture = platform.machine()
    processor = platform.processor()
    ram = f"{round(psutil.virtual_memory().total/(1024**3))} GB"
    return {"architecture": architecture, 
            "processor": processor, 
            "ram": ram,
            "free_storage": free_storage,
            "used_storage": f"{stored_data_size} B"}

    

if __name__ == "__main__":
    app.run(host="localhost", port=1353, debug=True)