import hashlib
import base64
import os

def hasher(arquivo,d,n):
    with open (arquivo, "rb") as f:
        mensagem = f.read()
    hash = hashlib.sha3_256(mensagem)
    hashbytes = hash.digest()
    hashint = int.from_bytes(hashbytes,byteorder='big')
    assinatura = pow(hashint,d ,n)
    assinaturabytes = assinatura.to_bytes((n.bit_length()+7)//8,byteorder='big')
    assinatura64 = base64.b64encode(assinaturabytes).decode('utf-8')
    with open (arquivo+".sig","w") as fsig:
        fsig.write(assinatura64)
