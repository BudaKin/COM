import komm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")  # ou "Qt5Agg"

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

# 2. Escreva um programa que simule a probabilidade de erro de bit de um sistema de
# comunicação que utiliza o código convolucional mostrado na figura abaixo com decodificação 
# via algoritmo de Viterbi no canal BSC(𝑝). Considere a transmissão de 1000 quadros, 
# cada qual contendo ℎ = 200 blocos de informação e p variando de 0 a 1/2

h = 200 # número de blocos de informação
n_quadros = 1000 # número de quadros

p = np.linspace(0, 0.5, 10) # p variando de 0 a 1/2


convcode = komm.ConvolutionalCode([[0b1111001, 0b1011011]]) # codigo convolucional seguindo as matrizes geradoras

nkµ = (convcode.num_output_bits, convcode.num_input_bits, convcode.memory_order)
print(f"(n,k,µ) = ",nkµ)

coder = komm.TerminatedConvolutionalCode(convolutional_code=convcode, num_blocks=h) # terminação do código

decoder = komm.ViterbiDecoder(code=coder) # decodificador de Viterbi

source = komm.DiscreteMemorylessSource(2) # Padrão dos dados transmitidos

BER_list = []

for p_i in p:
    bsc_p = komm.BinarySymmetricChannel(p_i) # canal variando p de 0 a 1/2
    u = source.emit((h,n_quadros)) # mensagem
    v = coder.encode(u) # Codificando a mensagem u através do código convolucional
    b = bsc_p.transmit(v) # Transmissão pelo canal com erro p_i
    u_hat = decoder.decode(b) # Decodificação Viterbi

    BER_list.append(np.mean(u != u_hat)) # BER do codigo convolucional

fig, ax = plt.subplots()

ax.semilogy(p, BER_list, "C0")
ax.set_xlabel("Pb")
ax.set_ylabel("BER")

ax.grid()
plt.show()
