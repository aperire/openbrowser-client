import random
import numpy as np
from PIL import Image

class Client:
    def __init__(self):
        pass

    def get_enc_key(
        self,
        pixel_n # number of pixels
    ):
        # create a random array to encrypt original file
        enc_key = [[random.randint(0,256) for j in range(3)] for i in range(pixel_n)]
        return enc_key

    def process_img_to_block(
        self,
        img_path, # path to image
        enc_key, # encryption key
        block_size # size of pixels in a single block
    ):
        img = Image.open(img_path)
        raw_rgb_array = np.array(img)

        # Convert rgb array to 1D array
        rgb_array = []
        cnt = 0
        for i in range(len(raw_rgb_array)):
            for j in range(len(raw_rgb_array[i])):
                pix = raw_rgb_array[i][j]
                encryption = enc_key[cnt]
                enc_pix = [i+j for i, j in zip(pix, encryption)]
                rgb_array.append(enc_pix)
                print(f"{100*cnt/(raw_rgb_array.shape[0]*raw_rgb_array.shape[1])}%")
                cnt+=1



client = Client()
enc_key = client.get_enc_key(6016**2)
print(client.process_img_to_block(
    "img.jpeg",
    enc_key,
    0
    )
)