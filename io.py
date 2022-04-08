from Crypto.Cipher import AES , PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from Crypto.Random import get_random_bytes
import json


with open('sessionKey\\admin.json') as f:
    data = json.load(f)

b4= json.loads(data)

print(b4['iv'])
# with open(input("URL:"),'rb') as f:
#     byte_read = f.read()
 
# encrypted_data = byte_read
 
# filesize = len(encrypted_data)
 
# print("filesize:" , filesize)
 
# sec_key = get_random_bytes(16)
 
# cipher = AES.new(sec_key,AES.MODE_CBC)
 
# print(sec_key)
 
# # iv = b'0000000000000000'
# iv = cipher.iv

# print(iv)
 

 
# # AES encryption
 
# chiper_text = cipher.encrypt(pad(byte_read,AES.block_size))



# with open('Capture001.png','wb') as f:
#     f.write(chiper_text)

# with open("C:\\Users\\AJBas\\Desktop\\Projects\\IS-project\\Capture001.png", 'rb') as f:
#     g = f.read()
    # f.write(chiper_text)

# print(g)


# try:
#     f = b'\x12\xc1_A\xe7X\xa1\xa7\x94\x89\xb8H\xc6b\x90\x0b'

#     iv = b'}g9v]\x82\xf1$\xb6ZV\x14\xd2;\x0c\xd9'
#     cipher = AES.new(f, AES.MODE_CBC, iv)
#     data = unpad(cipher.decrypt(g), AES.block_size)
#     # print("The message was: ", data)
# except (ValueError, KeyError):
#     pass

# with open('Capture001.png','wb') as f:
#     f.write(data)
