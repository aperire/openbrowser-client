from openbrowser import Client
import requests



client = Client("")
enc_key = client.get_enc_key(200*200)


# rpc_array = ["gr", "ge", "e"]
# client.process_img(
#     "img.png",
#     enc_key,
#     rpc_array
# )

status = client.ping_rpc(["http://127.0.0.1:5000"])
print(status)


push = client.distribute_block_to_rpc(
    "t3wgw",
    [1],
    ["http://127.0.0.1:5000"]
)

print(push)