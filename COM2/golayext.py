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

EbN0_dB_list = st.slider(label="Eb/N0 (dB)", min_value=-2.0, max_value=6.0, value=1.0, step=1.0)  # Eb/N0 variando de  -2 a 6 dB.
EbN0= 10**(EbN0_dB_list/10)

awgn = komm.AWGNChannel(signal_power=1.0, snr=1.0/EbN0) # Canal AWGN com Eb/𝑁0  variando de −2 a 6 dB.
qpsk = komm.PSKConstellation(4) # Modulação BPSK.'
code = komm.GolayCode(True) # Código de Golay estendido (24, 12).
decoder = komm.ExhaustiveSearchDecoder(code) # Decodificação hard de mínima distância.

cols = st.columns(3)

with cols[0]:
    # Código antes da transmissão e sem codificação
    pass
    
with cols[1]:
    # Código após tranmissão usando codificação Golay extendido
    pass

with cols[2]:
    # Código após tranmissão sem codificação
    pass
