import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import komm

from amostragem import amostragem, reconstrucao

def m(t: float) -> float:
    return 6 * np.sin(2*np.pi*t) - 0.00001

def main():
    st.title("Conversão A/D")
    col1, col2 = st.columns(2)
    with col1:
        fa = st.slider(
            label="Taxa de Amostragem $f_a$:",
            min_value=2,
            max_value=16,
            step=1,
            value=8,
            format="%d amostras/s"
        )
    with col2:
        L = st.select_slider(
            label="Número de níveis de quantização disponíveis $L$:",
            options=[2,4,8,16,32,64,128,256],
            value=16,
        )

    Ta = 1/fa
    Nb = int(np.log2(L))
    quantizer = komm.UniformQuantizer(
        num_levels= L,
        input_range= (-8, 8),
        choice="mid-riser",
    )
    tab1,tab2 = st.tabs(["Quantizador","Sinais"])
    with tab1:
        x = np.linspace(-10, 10, 1000)
        y = quantizer.quantize(x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title("Curva Entrada $\\times$ Saída")
        ax.set_xlabel("Entrada")
        ax.set_ylabel("Saída")
        ax.grid()
        st.pyplot(fig)

    with tab2:
        a, b = (-0.5, 0.5)
        times = np.linspace(a, b, 1000)
        Na = int((b - a)/Ta)
        
        fig, ax = plt.subplots()
        ax.plot(
            times,
            [m(t) for t in times],
            label="$m(t)$",
            color='r',
        )

        instantes, amostras = amostragem(m,Ta,a,Na)
        ax.plot(
            instantes,
            amostras,
            linestyle="None",
            marker="o",
            label="$m[n]$",
            color='r',
        )

        amostras_q = quantizer.quantize(amostras)
        ax.plot(
            instantes,
            amostras_q,
            linestyle="None",
            marker="o",
            label="$m_q[n]$",
            color='b',
        )
        m_hat = reconstrucao(amostras_q, a, Ta) # type: ignore
        ax.plot(
            times,
            [m_hat(t) for t in times],
            label="$\\hat(m)(t)$",
            color='b',
        )

        ax.grid()
        ax.set_xlabel("$t$ [s]")
        ax.legend()
        st.pyplot(fig)

main()