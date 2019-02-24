# -*- coding:utf-8 -*-
"""AES encrypt"""
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64
def encrypt_AES(data, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    data = pad(data, AES.block_size, style='pkcs7')
    ret = base64.b64encode(aes.encrypt(data))
    return ret
