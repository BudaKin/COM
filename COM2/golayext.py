import streamlit as st
import komm
import numpy as np
import matplotlib.pyplot as plt

# Escreva um programa que simule a probabilidade de erro de bit de um sistema de comunicação com as seguintes características:
# • Canal AWGN com Eb/𝑁0  variando de −2 a 6 dB.
# • Modulação BPSK (simule em banda base).
# • Código de Golay estendido (24, 12), com decodificação hard de mínima distância.
# Compare com o caso não codificado.

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

st.title("Questão 2: Código de Golay Estendido")

EbN0_dB_list = np.arange(-2, 7)  # Eb/N0 variando de  -2 a 6 dB.
EbN0 = 10**(EbN0_dB_list/10)

# awgn = komm.AWGNChannel(signal_power=1.0, snr=EbN0) # Canal AWGN com Eb/𝑁0  variando de −2 a 6 dB.
bpsk = komm.PSKConstellation(2) # Modulação BPSK.
code = komm.GolayCode(True) # Código de Golay estendido (24, 12).
code = komm.BlockCode([[1]]) # Código sem codificação (n,n).
decoder = komm.ExhaustiveSearchDecoder(code) # Decodificação hard de mínima distância.

source = komm.DiscreteMemorylessSource(2) # Padrão dos dados transmitidos

Eb = bpsk.mean_energy() / code.rate

print(Eb)
 
u = source.emit(10000) # Dados Transmitidos

v = code.encode(u) # Codificação Cod Golay

mod_v = bpsk.indices_to_symbols(v) # Modular BPSK

b = awgn.transmit(mod_v) # Transmissão no canal

demod_b = bpsk.closest_indices(b) # Demodular BPSK

u_hat = decoder.decode(demod_b) # Decodificação Cod Golay

BER = np.mean(u != u_hat)

Pb = komm.gaussian_q(np.sqrt(2*EbN0))

cols = st.columns(2)

with cols[0]:
    # Código após tranmissão usando codificação Golay extendido
    pass
    
with cols[1]:
    # Código após tranmissão sem codificação
    pass
