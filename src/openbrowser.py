import numpy as np
from PIL import Image
import requests
from hashlib import sha256
import math

class Encryption:
    def __init__(self):
        pass

    def power_check(self, n: int, base: int):
        assert n>=0, "Index cannot be negative"
        if n==0:
            return True
        else:
            return math.log(n,base).is_integer()


    def encrypt_rgb_array(self, rgb_array: np.array, action: list, condition: list):
        '''
        action = {
            "a": "add",
            "s": "subtract"
        }

        condition = {
            "M": "every geometric sequence n index",
            "P": "every power of n index",s
        }
        '''
        for i in condition:
            cn = int(i[1:])
            if i[0] == "M":
                for j in action:
                    an = int(j[1:]) 
                    if j[0] == "a":
                        rgb_array = [rgb_array[rgb_index]+an if rgb_index%cn==0 else rgb_array[rgb_index] for rgb_index in range(len(rgb_array))]
                    if j[0] == "s":
                        rgb_array = [rgb_array[rgb_index]-an if rgb_index%cn==0 else rgb_array[rgb_index] for rgb_index in range(len(rgb_array))]
                        
            if i[0] == "P":
                for j in action:
                    an = int(j[1:])  
                    if j[0] == "a":
                        rgb_array = [rgb_array[rgb_index]+an if self.power_check(rgb_index,cn) else rgb_array[rgb_index] for rgb_index in range(len(rgb_array))]
                    if j[0] == "s":
                        rgb_array = [rgb_array[rgb_index]-an if self.power_check(rgb_index,cn) else rgb_array[rgb_index] for rgb_index in range(len(rgb_array))]
        return np.array(rgb_array, dtype=np.int8)

    def decrypt_rgb_array(self, rgb_array: np.array, action: list, condition: list):

        '''
        p3 s2
        M3 M2
        1. M3 -> p3, s2
        2. M2 -> p3, s2
        '''
        for i in reversed(condition):
            cn = int(i[1:])
            if i[0] == "M":
                for j in reversed(action):
                    an = int(j[1:])  
                    if j[0] == "p":
                        rgb_array = [(rgb_array[rgb_index]**(1/an)).astype(int) if rgb_index%cn==0 else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
                    if j[0] == "a":
                        rgb_array = [(rgb_array[rgb_index]-an).astype(int) if rgb_index%cn==0 else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
                    if j[0] == "s":
                        rgb_array = [(rgb_array[rgb_index]+an).astype(int) if rgb_index%cn==0 else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
                    if j[0] == "m":
                        rgb_array = [(rgb_array[rgb_index]/an).astype(int) if rgb_index%cn==0 else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
            if i[0] == "P":
                for j in reversed(action):
                    an = int(j[1:])  
                    if j[0] == "p":
                        rgb_array = [(rgb_array[rgb_index]**(1/an)).astype(int) if self.power_check(rgb_index,cn) else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
                    if j[0] == "a":
                        rgb_array = [(rgb_array[rgb_index]-an).astype(int) if self.power_check(rgb_index,cn) else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
                    if j[0] == "s":
                        rgb_array = [(rgb_array[rgb_index]+an).astype(int) if self.power_check(rgb_index,cn) else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
                    if j[0] == "m":
                        rgb_array = [(rgb_array[rgb_index]/an).astype(int) if self.power_check(rgb_index,cn) else (rgb_array[rgb_index]).astype(int) for rgb_index in range(len(rgb_array))]
        return np.array(rgb_array, dtype=np.int8)

class Client:
    def __init__(self, connection: str):
        self.connection = connection
        self.encryption = Encryption()

    def get_available_rpcs(self):
        """
        Get RPCs that are online
        
        Example:
            >>> rpc_array = client.get_available_rpcs()
            [
                "https://localhost:3000",
                "https://localhost:5000"
            ]
        
        Returns:
            Type: list
            RPCs in registry
        """
        rpc_array = requests.get(f"{self.connection}/rpc").json()
        return rpc_array

    def process_img(
        self,
        action: list,
        condition: list,
        img_path: str,
        rpc_array: list
    ):
        """ 
        Process image prior to RPC request
        
        Args:
            action: action key for encryption
            condition: condition key for encryption
            img_path: path to image file
            rpc_array: list of selected RPCs to transfer data
            
        Example: 
            >>> enc_rgb_array, private_key, public_key = client.process_img(
                action=["a3", "m2"],
                condition=["M4", "M17"],
                img_path="./img.png",
                rpc_array=["http://localhost:3000"]
            )
        """
        # open image and get rgb array
        img = Image.open(img_path)
        raw_rgb_array = np.array(img, dtype=np.int8)
        shape = raw_rgb_array.shape
        
        # change shape to linear rgb: .reshape(1, y*x, 3: rgb)
        rgb_array = raw_rgb_array.reshape(1, shape[0]*shape[1], 3)[0]
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
            "enc": (action, condition),
            "rng": range_array,
            "rpc": rpc_array
        }

        # get public key
        public_key = str(sha256(str(private_key).encode('utf-8')).hexdigest())
        return np.array(enc_rgb_array), private_key, public_key

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
            json_data = {public_key: (enc_rgb_array[i]).tolist()}

            r = requests.post(f"{rpc_array[i]}/data", json=json_data)

        return True
    
    def retrieve_block_from_rpc(
        self,
        public_key: str,
        private_key: dict,
        retrieve_dir: str,
        file_name: str
    ):
        # decompose private key
        dim = private_key["dim"]
        action, condition = private_key["enc"]
        rng = private_key["rng"]
        rpc_array = private_key["rpc"]
        
        # request data from rpc array
        encrypted_rgb_array = []
        for rpc in rpc_array:
            data = requests.post(f"{rpc}/retrieve", json={"pubkey": public_key}).json()["data"]
            encrypted_rgb_array=encrypted_rgb_array+data
        
        encrypted_rgb_array = np.asarray(encrypted_rgb_array).reshape(1, dim[0]*dim[1], 3)[0]
        # decrypt the rgb array
        decrypted_rgb_array = self.encryption.decrypt_rgb_array(
            encrypted_rgb_array, action, condition
        )
        # reshape the rgb array
        rgb_array = np.asarray(decrypted_rgb_array).reshape(dim[0], dim[1], 3).astype(np.uint8)

        img = Image.fromarray(rgb_array)

        img.save(f"{retrieve_dir}/{file_name}")
        
        return rgb_array