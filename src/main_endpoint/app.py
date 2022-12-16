from flask import Flask

app = Flask(__name__)

rpc_array = [
    "http://localhost:8080"
]

@app.route("/rpc", methods=["GET"])
def rpc_registry():
    return rpc_array

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)