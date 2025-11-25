from collections import Counter

import numpy as np
import komm
import matplotlib.pyplot as plt

with open("Alice.txt", "rb") as f:
    livro = f.read()
    livro = [int(x) for x in livro]

freq = Counter(livro)

pmf = np.zeros(128, dtype=float)
for i in range(128):
    pmf[i] = freq[i] / freq.total()

code = komm.HuffmanCode(pmf=pmf)
encoded = code.encode(livro)


tam_original = len(livro) * 7
tam_comprimido = encoded.size

print(f"Tamanho original    : {tam_original}")
print(f"Tamanho comprimido  : {tam_comprimido}")
print(f"% do tamanho original : {tam_comprimido / tam_original:.2%}")

# plt.figure()
# plt.bar(np.arange(128),pmf)
# plt.show()