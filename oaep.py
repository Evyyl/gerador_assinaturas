from hashlib import sha3_256
from os import urandom
from math import ceil
from operator import xor

def mask(data, seed, mlen, hash_func=sha3_256):
    txt = b''
    hash_size = hash_func().digest_size
    for i in range(ceil(mlen / hash_size)):
        c = i.to_bytes(4, "big")
        txt += hash_func(seed + c).digest()
    return bytes(map(xor, data, txt[:mlen]))

def cifra_oaep(n, mensagem, hash_func=sha3_256):
    k = (n.bit_length() + 7) // 8
    tam_msg = len(mensagem)
    tam_hash = hash_func().digest_size

    limite = k - 2 * tam_hash - 2

    if tam_msg > limite:
        raise ValueError(f"Mensagem muito longa. Máximo permitido: {limite} bytes")

    label_hash = hash_func(b"").digest()

    padding_string = b"\x00" * (k - tam_msg - 2 * tam_hash - 2)
    data_block = label_hash + padding_string + b'\x01' + mensagem

    seed = urandom(tam_hash)

    masked_data_block = mask(data_block, seed, k - tam_hash - 1, hash_func)
    masked_seed = mask(seed, masked_data_block, tam_hash, hash_func)

    return b'\x00' + masked_seed + masked_data_block

def decifra_oaep(n, msg_cifrada, hash_func=sha3_256):
    k = (n.bit_length() + 7) // 8
    tam_hash = hash_func().digest_size

    _, masked_seed, masked_data_block = (
        msg_cifrada[:1], 
        msg_cifrada[1:1 + tam_hash], 
        msg_cifrada[1 + tam_hash:]
    )

    seed = mask(masked_seed, masked_data_block, tam_hash, hash_func)
    data_block = mask(masked_data_block, seed, k - tam_hash - 1, hash_func)
    data_block_sem_hash = data_block[tam_hash:]
    idx = data_block_sem_hash.find(b'\x01')

    if idx == -1:
        raise ValueError("Formato OAEP inválido")

    msg = data_block_sem_hash[idx + 1:]

    _, msg = data_block.split(b'\x01')
    return msg
