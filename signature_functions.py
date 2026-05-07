import hashlib
import base64
import os

import oaep_functions as oaep

# Define if wants to use oaep:
with_oaep = False

def hasher(arquivo,d,n):
    # Read file:
    with open (arquivo, "rb") as f: mensagem = f.read()
    
    # Hash file:
    hash = hashlib.sha3_256(mensagem)
    hashbytes = hash.digest()
    print(f"\n{hashbytes = }")

    # Cryptography Hash with OAEP RSA:
    if with_oaep:
        # OAEP Hash:
        oaep_hashbytes = oaep.cifra_oaep(n, hashbytes)
        print(f"\n{oaep_hashbytes = }")

        # Cryptography OAEP Hash with RSA:
        hashint = int.from_bytes(oaep_hashbytes,byteorder='big')
        assinatura = pow(hashint,d ,n)
        assinaturabytes = assinatura.to_bytes((n.bit_length()+7)//8,byteorder='big')
    
    # Cryptography Hash with RSA:
    if not with_oaep:
        hashint = int.from_bytes(hashbytes,byteorder='big')
        assinatura = pow(hashint,d ,n)
        assinaturabytes = assinatura.to_bytes((n.bit_length()+7)//8,byteorder='big')

    # Signature save (in str):
    assinatura64 = base64.b64encode(assinaturabytes).decode('utf-8')
    with open (arquivo+".sig","w") as fsig: fsig.write(assinatura64)

    # Signature save for posterior parsing: (Second line)
    with open ("binaries","a") as f: f.write("\n" + assinatura64)

def verificar_assinatura(arquivo, assinatura_arquivo, e, n):

    # Original file hash:
    print(f"== Original file hash: ==")
    with open(arquivo, "rb") as f: mensagem = f.read()

    hash_atual = hashlib.sha3_256(mensagem).digest()
    print(f"\n{hash_atual = }")

    hash_atual_int = int.from_bytes(hash_atual, byteorder='big')
    print(f"\n{hash_atual_int = }")

    with open(assinatura_arquivo, "r") as f: linhas = f.readlines()

    # For signature with hash with no oaep:
    if not with_oaep:
        print(f"\n== Recovering hash from recived signature: ==")
        assinatura64 = linhas[0].strip()
        print(f"\n{assinatura64 = }")
        assinatura_bytes = base64.b64decode(assinatura64)
        print(f"\n{assinatura_bytes = }")
        assinatura_int = int.from_bytes(assinatura_bytes, byteorder='big')
        print(f"\n{assinatura_int = }")
        hash_recuperado = pow(assinatura_int, e, n)

    # For signature with hash with oaep:
    if  with_oaep:
        assinatura64 = linhas[0].strip()
        print(f"\n{assinatura64 = }")
        assinatura_bytes = base64.b64decode(assinatura64)
        print(f"\n{assinatura_bytes = }")
        hash_recovered = oaep.decifra_oaep(n, assinatura_bytes)
        print(f"\nbinario:{hash_recovered = }")
        assinatura_int = int.from_bytes(hash_recovered, byteorder='big')
        print(f"\n{assinatura_int = }")
        hash_recuperado = pow(assinatura_int, e, n)

    print(f"\n== Comparing file hash with its hash signature: ==")
    print(f"\n{hash_recuperado = }")
    print(f"\n{hash_atual_int = }\n")

    return print(hash_recuperado == hash_atual_int)

