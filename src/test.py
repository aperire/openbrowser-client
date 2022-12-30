from openbrowser import Client, Encryption
import requests
import random
import json
from PIL import Image
import numpy as np

# Initialize Client
client = Client("http://localhost:3000")

# Fetch RPC from main endpoint
rpc_array = client.get_available_rpcs()

# Ping RPC
off_rpc_array = client.ping_rpc(rpc_array)
assert len(off_rpc_array)==0, "Certain RPCs are unavailable"

# Set constant
condition = ["M2", "P2", "M5"]
action = ["a52", "s18"]
img_path = "./img/fd1.jpeg"

# Process Image
enc_rgb_array, private_key, public_key = client.process_img(
    action, condition, img_path, rpc_array
)

with open("private_key.json", "w") as f:
    json.dump(private_key, f)

# Post data to RPC
result = client.distribute_block_to_rpc(
    public_key,
    enc_rgb_array,
    rpc_array
)

# Retrieve data from RPC
rgb_array = client.retrieve_block_from_rpc(
    public_key,
    private_key,
    "retrieve_img",
    "fd1.jpeg"
)