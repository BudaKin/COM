import streamlit as st
import komm
import numpy as np
import matplotlib.pyplot as plt

st.title("Códigos de bloco")

filename = "mario.txt"

with open(filename) as f:
    image = []
    for line in f:
        line = [int(x) for x in line.strip()]
        image.append(line)
    image = np.array(image)
    image = np.kron(image, np.ones((7,7), dtype=int))
    height, width = image.shape

    def plot_bits(bits):
        image_bits = bits.reshape(height, width)
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.matshow(image_bits, cmap="binary")
        st.pyplot(fig)
    
    p = st.slider(label="Probabilidade de troca do BSC ($p$)", min_value=0.0, max_value=0.5, value=0.08)

    bsc = komm.BinarySymmetricChannel(p)

    cols = st.columns(2)

    u = image.reshape(height*width)

    with cols[0]:
        plot_bits(u)

    # Não codificado
    b_nc = bsc.transmit(u)
    with cols[1]:
        plot_bits(b_nc)

    