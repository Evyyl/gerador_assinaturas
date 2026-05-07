""" Sign chosen file.

    Create two files:
        'binaries' that ends up with:
            file encoded in base64;
            signature encoded in base64
            public key exponente encoded in base64; and
            public kwy modulus encoded in base64.

        '`file_name`.sig' from signature.py that contains:
            signature encoded in base64

"""

import keygen_functions as keygen
import signature_functions as signature
import base64

# File to sign:
file_name = "exemplo.jpeg"

# File binary code encoded with base64 for posterior parsing: (First line)
print(f"\n{file_name = }")
with open(file_name, "rb") as f: file_content = f.read()
print(f"\n{file_content = }")
file_binary = base64.b64encode(file_content)
file_binary_base64 = file_binary.decode('utf-8')
with open("binaries", "w") as f: f.write(file_binary_base64)

# Generate primes:
primos = keygen.gerarprimos()
print(f"\n{primos = }")

# Generate keys:
chaves = keygen.gerarchave(primos[0], primos[1])
print(f"\n{chaves = }")

# Sign the file:
signature.hasher(file_name,chaves[1][0],chaves[1][1])

# Public key exp save for posterior parsing: (Third line)
public_key_exp = chaves[0][0]
print(f"\n{public_key_exp = }")
public_key_exp = public_key_exp.to_bytes((public_key_exp.bit_length() + 7) // 8, byteorder='big')
print(f"\n{public_key_exp = }")

#TEST Public key exp recover test: (delete next 2 lines)
#public_key_exp_recover = int.from_bytes(public_key_exp, byteorder='big')
#print(f"\n{public_key_exp_recover = }")

public_key_exp = base64.b64encode(public_key_exp).decode('utf-8')
print(f"\n{public_key_exp = }")

with open("binaries", "a") as f: f.write("\n" + str(public_key_exp))

# Public key modulus save for posterior parsing: (Fourth line)
public_key_mod = chaves[0][1]
print(f"\n{public_key_mod = }")
public_key_mod = public_key_mod.to_bytes((public_key_mod.bit_length() + 7) // 8, byteorder='big')
print(f"\n{public_key_mod = }")

#TEST Public key mod recover test: (delete next 2 lines)
#public_key_mod_recover = int.from_bytes(public_key_mod, byteorder='big')
#print(f"\n{public_key_mod_recover = }")

public_key_mod = base64.b64encode(public_key_mod).decode('utf-8')
print(f"\n{public_key_mod = }")

with open("binaries", "a") as f: f.write("\n" + str(public_key_mod))

