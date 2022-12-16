from openbrowser import Client, Encryption
import requests


# Initialize Client
# client = Client("http://localhost:3000")

# #Fetch RPC from main endpoint
# rpc_array = client.get_available_rpcs()
#print(rpc_array)

# Process Image
enc = Encryption()
array = [1,2,3,4,5,6,7,8]

enc_array = enc.encrypt_rgb_array(
    array,
    ["a1", "p2"],
    ["M2"]
)
print(enc_array)

# # # Ping RPC
# status = client.ping_rpc(rpc_array)
# print(status)

# # Post data to RPC
# push = client.distribute_block_to_rpc(
#     "tegjwohpgqejp0",
#     ["miyeon"],
#     rpc_array
# )

# print(push)