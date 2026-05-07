""" Verify if signature is genuine.

    Read file, it's hash and sender's public key (e and n) binaries from
    'binaries' file, and applies it to verificar_assinatura() in 
    signature module.

    verificar_assinatura() from signature module print if it's true.

"""

import os
import signature_functions as signature
import base64

with open("binaries", "r") as f:
    lines = [f.readline().strip() for _ in range(4)]

file_b64, file_hash_b64, public_key_exp_b64, key_modulus_b64 = lines

print(f"\n== Binaries present on 'binaries' files: ==")
print(f"\n{file_b64 = }")
print(f"\n{file_hash_b64 = }")
print(f"\n{public_key_exp_b64 = }")
print(f"\n{key_modulus_b64 = }")
print(f"\n")

key_modulus = int.from_bytes(base64.b64decode(key_modulus_b64) , byteorder='big')
public_key_exp = int.from_bytes(base64.b64decode(public_key_exp_b64) , byteorder='big')

# How signature module read the files in folder we are passing the file
# names, but the signature module show that they are the same from
# 'binaries' file.
signature.verificar_assinatura("exemplo.jpeg", "exemplo.jpeg.sig", public_key_exp, key_modulus)

