import random
import numpy as np
from PIL import Image
import requests
from hashlib import sha256
from flask import Flask

class Encryption:
    def __init__(self):

class Client:
    def __init__(self, connection: str):
        self.connection = connection

    def get_available_rpcs(self):
        rpc_array = requests.get(self.connection).json
        return rpc_array
    
    def get_enc_key(
        self,
        pixel_n: int
    ):
        
        # constraint: enc_key = (uint64, str<4)
     
        enc_key = {
            "action": "p3s5",
            "condition": ["M4", "P2"]
        }

        action = {
            "p": "power of",
            "a": "add",
            "s": "subtract",
            "m": "multiply"
        }

        condition = {
            "M": "every geometric sequence n index",
            "P": "every power of n index",
            "F": "every fibonacci starting with n"
        }



        """ 
        Returns 1D array of encryption key
        
        Args:
            pixel_n: Number of pixels in image

        Example: 
            >>> from openbrowser import Client
            >>> client = Client()
            >>> enc_key = client.get_enc_key(6016*6016)
        """
        # create a random array to encrypt original file
        enc_key = [[random.randint(0,256) for j in range(3)] for i in range(pixel_n)]
        return enc_key

    def process_img(
        self,
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
        enc_rgb_array = np.add(rgb_array, enc_key)

        # distribute pixels for each RPCs
        enc_rgb_array = np.array_split(enc_rgb_array, len(rpc_array))
        range_array = [len(i) for i in enc_rgb_array]

        # get private key
        private_key = {
            "dim": (shape[0], shape[1]),
            "enc": enc_key,
            "rng": range_array,
            "rpc": rpc_array
        }

        # get public key
        public_key = sha256(str(private_key).encode('utf-8')).hexdigest()
        
        return enc_rgb_array, private_key, public_key

    def distribute_block_to_rpc(self, 
        public_key: str, 
        enc_rgb_array: list, 
        rpc_array: list
    ):
        assert len(enc_rgb_array)==len(rpc_array), "num of rpc and block is different"

        # ping check

        # post data
        for i in range(len(rpc_array)):
            r = requests.post(rpc_array[i], json={public_key: enc_rgb_array[i]})
            
            



