import keygen
import signature

p, q = keygen.gerarprimos()
print ("O valor de p é :\n", p)
print ("O valor de q é :\n", q)

pub, priv = keygen.gerarchave(p, q)
e, n = pub
d, n = priv

print("Chave Pública: \n", pub)
print("Chave Privada: \n", priv)

signature.hasher("exemplo.jpeg", d, n) # Utiliza a chave privada
valido = signature.verificar_assinatura("exemplo.jpeg","exemplo.jpeg.sig",e,n) # Utiliza a chave publica
print("A assinatura é válida ?", valido)
