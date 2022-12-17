from openbrowser import Client, Encryption
import requests
import random
import json
from PIL import Image
import numpy as np

# Initialize Client
client = Client("http://localhost:3000")
encryption = Encryption()
condition = ["M2"]
action = ["p2"]
array = np.asarray([[13,12,199], [211,212,213]])
enc_array = encryption.encrypt_rgb_array(
    array,
    action,
    condition
)
dec_array = encryption.encrypt_rgb_array(
    enc_array,
    action,
    condition
)
print(array)
print(dec_array)
# # Fetch RPC from main endpoint
# rpc_array = client.get_available_rpcs()

# # Ping RPC
# off_rpc_array = client.ping_rpc(rpc_array)
# assert len(off_rpc_array)==0, "Certain RPCs are unavailable"

# # Set constant
# condition = ["M2"]
# action = ["p2"]
# img_path = "./img/fd.jpeg"

# # Process Image
# enc_rgb_array, private_key, public_key = client.process_img(
#     action, condition, img_path, rpc_array
# )

# with open("private_key.json", "w") as f:
#     json.dump(private_key, f)

# # Post data to RPC
# result = client.distribute_block_to_rpc(
#     public_key,
#     enc_rgb_array,
#     rpc_array
# )

# # Retrieve data from RPC
# retrieve_img = client.retrieve_block_from_rpc(
#     public_key,
#     private_key,
#     ""
# )
# print(retrieve_img)
