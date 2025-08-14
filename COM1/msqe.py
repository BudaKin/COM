import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def main() -> None:
    st.title("Análise do ruído de quantização para quantização uniforme")
    Nb = st.slider(
        label="Bits por amostra $N_b$:",
        min_value=1,
        max_value=8,
        value=4,
    )

    mp = 10
    m = np.random.uniform(-mp, mp, 1000000)
    L = 2**Nb
    quantizer = komm.UniformQuantizer(L, input_range=(-mp, mp))
    mq = quantizer.quantize(m)
    e = m - mq

    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.hist(e, bins=50, density=True, alpha=0.5, color="b")
    ax.set_title("Histograma do ruído de quantização")
    ax.set_xlabel("$e$")
    ax.set_ylabel("$f_e(e)$")
    ax.set_xlim(-6, 6)
    ax.set_ylim(0, 5)
    ax.grid()
    st.pyplot(fig)

    delta = quantizer.quantization_step
    e_max_teo = delta / 2
    e_max_sim = np.max(np.abs(e))
    msqe_teo = delta**2 / 12
    msqe_sim = np.mean(e**2)
    sqnr_teo = 4**Nb
    sqnr_sim = np.mean(m**2) / msqe_sim

    col1, col2, col3 = st.columns(3, border=True)
    col1.write("**Erro Máximo**")
    col1.metric(label="Teórico", value=f"{e_max_teo:g}")
    col1.metric(label="Simulado", value=f"{e_max_sim:g}")
    col2.write("**MSQE**")
    col2.metric(label="Teórico", value=f"{msqe_teo:g}")
    col2.metric(label="Simulado", value=f"{msqe_sim:g}")
    col3.write("**SQNR**")
    col3.metric(label="Teórico", value=f"{sqnr_teo:g}")
    col3.metric(label="Simulado", value=f"{sqnr_sim:g}")


if __name__ == "__main__":
    main()
