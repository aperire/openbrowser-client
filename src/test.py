from openbrowser import Client
import requests


# Initialize Client
client = Client("http://localhost:3000")

# Fetch RPC from main endpoint
rpc_array = client.get_available_rpcs()
print(rpc_array)


# Ping RPC
status = client.ping_rpc(rpc_array)
print(status)

# Post data to RPC
push = client.distribute_block_to_rpc(
    "t3wgw",
    [1],
    rpc_array
)

print(push)