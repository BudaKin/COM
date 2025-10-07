import komm
import numpy as np
import matplotlib.pyplot as plt
 
# code = komm.BlockCode([
#     [1, 0, 0, 0, 1, 1],
#     [0, 1, 0, 1, 0, 1],
#     [0, 0, 1, 1, 1, 0],
# ])
code = komm.GolayCode()
 
k, n = code.dimension, code.length
alpha = code.coset_leader_weight_distribution()
 
ps = np.linspace(0, 0.5, num=1000)
 
BLER_cod = 1 - sum(alpha[i] * ps**i * (1-ps)**(n-i) for i in range(n+1))
BLER_ncod = 1 - (1-ps)**k
 
plt.plot(ps, BLER_cod, label="Codificado")
plt.plot(ps, BLER_ncod, "--", label="Não codificado")
plt.xlabel("$p$")
plt.ylabel("$P_B$")
plt.legend()
plt.grid()
plt.show()