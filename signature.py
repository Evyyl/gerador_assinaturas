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
        
def verificar_assinatura(arquivo, assinatura_arquivo, e, n):

    with open(arquivo, "rb") as f:
        mensagem = f.read()

    hash_atual = hashlib.sha3_256(mensagem).digest()
    hash_atual_int = int.from_bytes(hash_atual, byteorder='big')

    with open(assinatura_arquivo, "r") as f:
        linhas = f.readlines()

    assinatura64 = linhas[0].strip()
    assinatura_bytes = base64.b64decode(assinatura64)
    assinatura_int = int.from_bytes(assinatura_bytes, byteorder='big')
    hash_recuperado = pow(assinatura_int, e, n)

    return hash_recuperado == hash_atual_int
