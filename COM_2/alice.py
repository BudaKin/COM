from collections import Counter

import numpy as np
import komm
import matplotlib.pyplot as plt

with open("Alice.txt", "rb") as f:
    livro = f.read()
    livro = [int(x) for x in livro]

freq = Counter(livro)
print(len(set(livro)))

pmf = np.zeros(128, dtype=float)
for i in range(128):
    pmf[i] = freq[i] / freq.total()

huff = komm.HuffmanCode(pmf=pmf)
encoded_huff = huff.encode(livro)

lz77 = komm.LempelZiv77Code(
    window_size=2**14,
    lookahead_size=16,
    source_cardinality=128
)
encoded_lz77 = lz77.encode(livro)
livro_hat = lz77.decode(encoded_lz77)
assert np.array_equal(livro, livro_hat)

tam_original = len(livro) * 7
tam_comprimido_huff = encoded_huff.size

print(f"Tamanho original    : {tam_original}")
print(f"Tamanho comprimido (Huff) : {encoded_huff.size}")
print(f"% do tamanho original : {encoded_huff.size / tam_original:.2%}")
print(f"Tamanho comprimido (Lz77) : {encoded_lz77.size}")
print(f"% do tamanho original : {encoded_lz77.size / tam_original:.2%}")

