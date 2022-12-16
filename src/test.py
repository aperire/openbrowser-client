from openbrowser import Client, Encryption
import requests
import random

# Initialize Client
# client = Client("http://localhost:3000")

# #Fetch RPC from main endpoint
# rpc_array = client.get_available_rpcs()
#print(rpc_array)

# Process Image
enc = Encryption()
# array = [1,2,3,4,5,6,7,8]

# enc_array = enc.encrypt_rgb_array(
#     array,
#     ["a1", "p2"],
#     ["M2"]
# )
testcases=list()
cnt=0
for i in range(0,100):
    test_pix_array=list()
    for j in range (0, random.randint(1,200)):
        test_pix_array.append(random.randint(1,256))
    testcases.append(test_pix_array)
for i in testcases:
    test_enc_array=enc.encrypt_rgb_array(
        i,
        ["a1", "p2"],
        ["M2"]
    )
    if not i==enc.decrypt_rgb_array(
        test_enc_array,
        ["a1", "p2"],
        ["M2"]
    ):
        print(i)
        print(test_enc_array)
        print(enc.decrypt_rgb_array(
        test_enc_array,
        ["a1", "p2"],
        ["M2"]
        ))
        print("fail")
        cnt+=1
print(cnt)
print("end of test")
# array=[244, 86, 89, 51, 61, 127, 85]
# enc_array=enc.encrypt_rgb_array(array,["a1","p2"],["M2"])
# print(enc_array)
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