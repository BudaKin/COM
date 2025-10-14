import streamlit as st
import komm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")  # ou "Qt5Agg"


# Questão 2: Código de Golay Estendido
# Escreva um programa que simule a probabilidade de erro de bit de um sistema de comunicação com as seguintes características:
# • Canal AWGN com Eb/𝑁0  variando de −2 a 6 dB.
# • Modulação BPSK (simule em banda base).
# • Código de Golay estendido (24, 12), com decodificação hard de mínima distância.
# Compare com o caso não codificado.

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

EbN0_dB_list = np.arange(-2, 7)  # Eb/N0 variando de -2 a 6 dB.
EbN0_list = 10**(EbN0_dB_list/10)

# awgn = komm.AWGNChannel(signal_power=1.0, snr=EbN0) # Canal AWGN com Eb/𝑁0  variando de −2 a 6 dB.
bpsk = komm.PSKConstellation(2) # Modulação BPSK.
code = komm.GolayCode(True) # Código de Golay estendido (24, 12).
# code = komm.BlockCode([[1]]) # Código sem codificação (n,n).
decoder = komm.ExhaustiveSearchDecoder(code) # Decodificação hard de mínima distância.

source = komm.DiscreteMemorylessSource(2) # Padrão dos dados transmitidos

Eb = bpsk.mean_energy() / code.rate

# print(Eb)

BER_cod_list = []
BER_ncod_list = []

for EbN0 in EbN0_list: 

    N0 = Eb/EbN0

    u = source.emit(12000) # Dados Transmitidos (Múltiplo de k)

    v = code.encode(u) # Codificação Cod Golay

    mod_v = bpsk.indices_to_symbols(v) # Modular BPSK

    awgn = rng.normal(loc=0, scale=np.sqrt(N0/2), size=v.size) # Canal AWGN com Eb/𝑁0  variando de −2 a 6 dB

    mod_b = awgn + mod_v # Transmissão no canal

    b = bpsk.closest_indices(mod_b) # Demodular BPSK

    u_hat = decoder.decode(b) # Decodificação Cod Golay

    BER_cod_list.append(np.mean(u != u_hat)) # BER Codificação

    BER_ncod_list.append(komm.gaussian_q(np.sqrt(2*EbN0))) # BER s/ Codificação

fig, ax = plt.subplots()

ax.semilogy(EbN0_dB_list, BER_cod_list, "C1", label= "Codificado")
ax.semilogy(EbN0_dB_list, BER_ncod_list, "C0", label="Não Codificado")
ax.set_xlabel("EB/N0 (dB)")
ax.set_ylabel("BER")
# ax.legend("Codificado","Não codificado")
ax.legend()

ax.grid()
plt.show()
