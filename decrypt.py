# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import fileio

def decrypt(ciphertext:bytes)->str:
	string=b'4A9745825F24883B657AFC4E4626A0F2253D8DE48C2B32D85F26989E9BFF78B9'
	key=string[:32]
	iv=string[:16]
	res=b''
	cipher=AES.new(key,AES.MODE_CBC,iv)
	plaintext=unpad(cipher.decrypt(ciphertext),AES.block_size)
	return plaintext.decode('utf-8')