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
        pass
    
    current_data.update(data)
    print(current_data)
    with open("storage.json", "w") as f:
        json.dump(current_data, f)

    return {"transfer": True}

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
            "used_storage": f"{stored_data_size} B"}

    

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)