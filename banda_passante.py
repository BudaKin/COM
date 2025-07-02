import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import komm.abc as abc

st.title("Modulação em banda passante")


def main():
    M = 4           # Ordem da modulação
    k = 2           # Número de bits por símbolo
    Rs = 20e3       # Taxa de símbolos (baud)
    Ts = 1 / Rs     # Intervalo de símbolo (s)
    sps = 500       # Amostras por símbolo
    fa = sps * Rs   # Frequência de amostragem (amostras/s)
    fc = 160e3      # Frequência da portadora

    mod_radio = st.radio(
        label="Modulação",
        options=["ASK", "PSK", "FSK"],
        horizontal=True,
    )

    def ask_mod():
        s_t = np.zeros_like(t)
        amplitudes = [0, 1, 2, 3]
        for i, s in enumerate(symbols):
            A = amplitudes[s]
            idx = slice(i*sps, (i+1)*sps)
            s_t[idx] = A * np.cos(2*np.pi*fc*t[idx])
        return s_t
    def psk_mod():
        s_t = np.zeros_like(t)
        fases = [0, np.pi/2, np.pi, 3*np.pi/2] # Phases
        for i, s in enumerate(symbols):
            phi = fases[s]
            idx = slice(i*sps, (i+1)*sps)
            s_t[idx] = np.cos(2*np.pi*fc*t[idx] - phi)
        return s_t
    def fsk_mod():
        s_t = np.zeros_like(t)
        Δf = 40e3
        frequencias = [fc + n*Δf/2 for n in [-3, -1, 1, 3]] # igualmente espaçadas, com centro = fc
        for i, s in enumerate(symbols):
            fi = frequencias[s]
            idx = slice(i*sps, (i+1)*sps)
            s_t[idx] = np.cos(2*np.pi*fi*t[idx])
        return s_t

    bits = np.array([0, 1, 0, 1, 1, 1, 0, 0, 1, 0])
    num_bits = len(bits)
    num_symbols = num_bits // k
    st.write(f"Bits: `{bits}`")

    # Mapeamento bits <--> símbolos
    gray = {
        (0, 0): 0,
        (0, 1): 1,
        (1, 1): 2,
        (1, 0): 3,
    }

    bits_reshaped = bits.reshape(-1, k)
    symbols = np.array([gray[tuple(k)] for k in bits_reshaped])
    st.write(f"Símbolos: `{symbols}`")

    t = np.arange(0, Ts*num_symbols, 1/fa)

    if mod_radio == "ASK":
        s_t = ask_mod()
    elif mod_radio == "PSK":
        s_t = psk_mod()
    else: 
        s_t = fsk_mod()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(t/1e-6, s_t)
    ax.set_xlabel("$t$ (µs)")
    ax.set_ylabel("$s(t)$")
    ax.grid()
    st.pyplot(fig)



if __name__ == '__main__':
    main()