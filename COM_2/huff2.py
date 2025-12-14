from collections import Counter

import numpy as np
import komm
import matplotlib.pyplot as plt

with open("alice2.txt", "rb") as f:
    livro = f.read()
    livro = [int(x) for x in livro]

freq = Counter(livro)
print(len(set(livro)))

pmf = np.zeros(256, dtype=float)
for i in range(256):
    pmf[i] = freq[i] / freq.total()

huff = komm.HuffmanCode(pmf=pmf)
encoded_huff = huff.encode(livro)

with open("alice2.bin", "wb") as f:
    f.write(encoded_huff)

decoded_huff = bytes(huff.decode(encoded_huff))

with open("alice2copys.txt", "wb") as f:
    f.write(decoded_huff)

tam_original = len(livro)
tam_comprimido_huff = encoded_huff.size/8
tam_decodificado_huff = len(decoded_huff)/8

#(a) A entropia da distribuição de frequências dos caracteres do livro.
print(f"Entropia: {komm.entropy(pmf):.4f} bits/símbolo")
#(b) O comprimento médio do código de Huffman obtido.
print(f"comprimento médio: {huff.rate(pmf):.4f} bits/símbolo")
#(c) O tamanho (em bytes) e a taxa de compressão do arquivo comprimido.
print(f"Tamanho original    : {tam_original}")
print(f"Tamanho comprimido (Huff) : {tam_comprimido_huff}")
print(f"% do tamanho original : {tam_comprimido_huff / tam_original:.2%}")
print(f"Tamanho Recuperado (Huff) : {tam_decodificado_huff}")
print(f"% do tamanho original : {tam_decodificado_huff / tam_original:.2%}")