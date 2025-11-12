import streamlit as st
import komm
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

st.title("Códigos de bloco")

filename = "mario.txt"

with open(filename) as f:
    image = []
    for line in f:
        line = [int(x) for x in line.strip()]
        image.append(line)
    image = np.array(image)
    image = np.kron(image, np.ones((4,4), dtype=int))
    height, width = image.shape

    def plot_bits(bits):
        image_bits = bits.reshape(height, width)
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.matshow(image_bits, cmap="binary")
        st.pyplot(fig)
    
    p = st.slider(label="Probabilidade de troca do BSC ($p$)", min_value=0.0, max_value=0.5, value=0.08)

    bsc = komm.BinarySymmetricChannel(p)
    # code = komm.HammingCode(3)
    code = komm.ReedMullerCode(1, 4)
    decoder = komm.SyndromeTableDecoder(code)

    st.write((code.length, code.dimension))
    st.write(f"**Minimum distance:** {code.minimum_distance()}")
    st.write(f"**Code rate:** {code.rate:.2%}")

    cols = st.columns(3)

    u = image.reshape(height*width)

    def get_ber(bits, bits_hat):
        return np.mean(bits != bits_hat)

    with cols[0]:
        plot_bits(u)
    
    with cols[1]:
        # Não codificado
        b_nc = bsc.transmit(u)
        plot_bits(b_nc)
        st.write(f"{get_ber(u, b_nc):.2%}")

    with cols[2]:
        # codificado
        v = code.encode(u)
        b_c = bsc.transmit(v)
        u_hat = decoder.decode(b_c)
        plot_bits(u_hat)
        st.write(f"{get_ber(u, u_hat):.2%}")

    