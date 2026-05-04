import keygen
import signature

primos = keygen.gerarprimos()
print (primos)
chaves = keygen.gerarchave(primos[0], primos[1])
print("\n")
print(chaves)
signature.hasher("exemplo.jpeg",chaves[1][0],chaves[1][1])

