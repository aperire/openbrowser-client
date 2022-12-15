from openbrowser import Client


client = Client("")
enc_key = client.get_enc_key(200*200)


rpc_array = ["gr", "ge", "e"]
client.process_img(
    "img.png",
    enc_key,
    rpc_array
)

'''
200, 200, 3
'''
