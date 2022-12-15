from flask import Flask, request
import json

app = Flask(__name__)

status = True

@app.route("/ping", methods=["GET"])
def set_rpc_status():
    return {"status": status}

@app.route("/data", methods=["POST"])
def get_data():
    data = request.json
    print(data)
    with open("storage.json", "w") as f:
        json.dump(data,f)
    return {"transfer": True}
    

if __name__ == "__main__":
    app.run(debug=True)