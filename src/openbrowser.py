import random
import numpy as np
from PIL import Image
import requests
from hashlib import sha256
from flask import Flask

class Encryption:
    def __init__(self):
        pass
    
    def encrypt_rgb_array(self, rgb_array: list, action: list, condition: list):
        '''
        action = {
            "p": "power of",
            "a": "add",
            "s": "subtract",
            "m": "multiply"
        }

        condition = {
            "M": "every geometric sequence n index",
            "P": "every power of n index",
        }
        '''
        for i in condition:
            cn = int(i[1:])
            if i[0] == "M":
                for j in action:
                    an = int(j[1:])  
                    if j[0] == "p":
                        rgb_array = [pix**an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
                    if j[0] == "a":
                        rgb_array = [pix+an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
                    if j[0] == "s":
                        rgb_array = [pix-an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
                    if j[0] == "m":
                        rgb_array = [pix*an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
            # need work @shpark
            if i[0] == "P":
                for j in action:
                    an = int(j[1:])  
                    if j[0] == "p":
                        rgb_array = [pix**an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
                    if j[0] == "a":
                        rgb_array = [pix+an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
                    if j[0] == "s":
                        rgb_array = [pix-an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]
                    if j[0] == "m":
                        rgb_array = [pix*an if rgb_array.index(pix)%cn==0 else pix for pix in rgb_array]

        return rgb_array


class Client:
    def __init__(self, connection: str):
        self.connection = connection
        self.encryption = Encryption()

    def get_available_rpcs(self):
        rpc_array = requests.get(f"{self.connection}/rpc").json()
        return rpc_array

    def process_img(
        self,
        action: list,
        condition: list,
        img_path: str,
        enc_key: list,
        rpc_array: list
    ):
        """ 
        Returns private key and 2D array of blocks
        
        Args:
            img_path: path to image file
            enc_key: encryption key generated from client.get_enc_key(pixel_n)
            rpc_array: list of selected RPCs to transfer data
            
        Example: 
            >>> from openbrowser import Client
            >>> client = Client()
            >>> enc_key = client.get_enc_key(6016*6016)
        """
        # open image and get rgb array
        img = Image.open(img_path)
        raw_rgb_array = np.array(img)
        shape = raw_rgb_array.shape
        
        # change shape to linear rgb: .reshape(1, y*x, 3: rgb)
        rgb_array = raw_rgb_array.reshape(1, shape[0]*shape[1], shape[2])[0]

        # encrypt each pixels
        enc_rgb_array = self.encryption.encrypt_rgb_array(
            rgb_array,
            action,
            condition
        )

        # distribute pixels for each RPCs
        enc_rgb_array = np.array_split(enc_rgb_array, len(rpc_array))
        range_array = [len(i) for i in enc_rgb_array]

        # get private key
        private_key = {
            "dim": (shape[0], shape[1]),
            "enc": [action, condition],
            "rng": range_array,
            "rpc": rpc_array
        }

        # get public key
        public_key = sha256(str(private_key).encode('utf-8')).hexdigest()
        
        return enc_rgb_array, private_key, public_key

    def ping_rpc(
        self,
        rpc_array: list
    ):
        # store unresponsive rpc
        off_rpc_array = []

        # ping all uri
        for uri in rpc_array:
            r = requests.get(f"{uri}/ping")
            if r.status_code != 200 or r.json()["status"] == False:
                off_rpc_array.append(uri)
        return off_rpc_array

    def distribute_block_to_rpc(
        self, 
        public_key: str, 
        enc_rgb_array: list, 
        rpc_array: list
    ):
        # check length of rgb array chunk and rpc array
        assert len(enc_rgb_array)==len(rpc_array), f"Number of chunk and RPC is different. \nChunk: {len(enc_rgb_array)}\nRPC: {len(rpc_array)}"

        # ping check
        off_rpc_array = self.ping_rpc(rpc_array)

        assert len(off_rpc_array)==0, f"Following RPCs are unresponsive \n{off_rpc_array}"

        # post data
        for i in range(len(rpc_array)):
            r = requests.post(f"{rpc_array[i]}/data", json={public_key: enc_rgb_array[i]})

        return True
            


