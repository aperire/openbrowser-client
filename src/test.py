from openbrowser import Client, Encryption
import requests
import random

# Initialize Client
client = Client("http://localhost:3000")

# Fetch RPC from main endpoint
rpc_array = client.get_available_rpcs()

# Ping RPC
off_rpc_array = client.ping_rpc(rpc_array)
assert len(off_rpc_array)==0, "Certain RPCs are unavailable"

# Set constant
condition = ["M4", "M17"]
action = ["a3", "m2", "s5"]
img_path = "./img.png"

# Process Image
enc_rgb_array, private_key, public_key = client.process_img(
    action, condition, img_path, rpc_array
)
print(public_key)

# Post data to RPC
result = client.distribute_block_to_rpc(
    public_key,
    enc_rgb_array,
    rpc_array
)

# Retrieve data from RPC