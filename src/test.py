from openbrowser import Client, Encryption
import requests


# Initialize Client
#client = Client("http://localhost:3000")

# Fetch RPC from main endpoint
# rpc_array = client.get_available_rpcs()
# print(rpc_array)

# Process Image
enc = Encryption()
array = [1,2,3,4,5,6,7,8]

enc_array = enc.encrypt_rgb_array(
    array,
    ["a4"],
    ["M2"]
)
print(enc_array)

# # Ping RPC
# status = client.ping_rpc(rpc_array)
# print(status)

# # Post data to RPC
# push = client.distribute_block_to_rpc(
#     "t3wgw",
#     [1],
#     rpc_array
# )

# print(push)