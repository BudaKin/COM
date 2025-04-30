import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import komm.abc as abc
from numpy.fft import fft, fftshift

def polar_mapping(bn):
    xn = 2*bn - 1
    return xn

def on_off_mapping(bn):
    xn = 1.0*bn
    return xn

def ami_mapping(bn):
    xn = np.zeros_like(bn, dtype=float) # vetor de zeros com tamanho do bn
    idx = np.flatnonzero(bn) # encontra o indice de valores não nulos
    n_ones = idx.size
    i = np.arange(n_ones)
    xn[idx] = (-1) ** i
    return xn

def main():
    A = 1.0
    Tb = 1.0

    pulse_menu = {
        "Retangular NRZ" : komm.RectangularPulse(1),
        "Retangular RZ" : komm.RectangularPulse(0.5),
        "Manchester" : komm.ManchesterPulse(),
    }
    mapping_menu = {
        "Polar": polar_mapping,
        "On-off": on_off_mapping,
        "AMI": ami_mapping,
    }
    st.title("Códigos de Linha")
    pulse_choice = st.segmented_control(
        label="Pulso:",
        options=pulse_menu.keys(),
        default="Retangular NRZ",
    )
    mapping_choice = st.segmented_control(
        label="Mapeamento:",
        options=mapping_menu.keys(),
        default="Polar",
    )
    if pulse_choice is None or mapping_choice is None:
        raise Exception("Nenhum Pulso/Mapeamento escolhido.")
    match (mapping_choice, pulse_choice):
        case("Polar","Retangular NRZ"):
            psd_teo = lambda f: A**2 * Tb * np.sinc(Tb * f)**2
        case _:
            raise ValueError("Combinação não implementada")

    pulse: abc.Pulse = pulse_menu[pulse_choice]
    mapping = mapping_menu[mapping_choice]
    tab1, tab2, tab3 = st.tabs(["Pulso", "Sinal", "PSD"])
    with tab1:
        t = np.linspace(-3, 3, 1000)
        pt = pulse.waveform(t)
        fig, ax = plt.subplots(1, 2)
        ax[0].plot(t, pt, 'C0')
        ax[0].set_xlabel("$t$")
        ax[0].set_ylabel("$p(t)$")
        ax[0].set_ylim(-1.2, 1.2)
        ax[0].grid()


        f = np.linspace(-4, 4, 1000)
        Pf = pulse.spectrum(f)
        ax[1].plot(f, Pf, 'C1')
        ax[1].plot(f, np.abs(Pf), 'C2')
        ax[1].set_xlabel("$f$")
        ax[1].set_ylabel("$P(f)$")
        ax[1].grid()

        fig.tight_layout()
        fig.set_figheight(4)
        st.pyplot(fig)

    Nbits = 10
    bn = np.array([1, 0, 0, 1, 1, 0, 1, 0, 1])
    st.write(f"Bits: {bn}")
    sps = 100 # Samples per symbol = samples/bit
    pam = komm.TransmitFilter(pulse, sps)
    xn = mapping(bn)
    yt = pam(xn)
    t = pam.time(xn)

    with tab2:
        fig, ax = plt.subplots(2,1)
        ax[0].stem(xn)
        ax[0].set_xlabel("$n$")
        ax[0].set_ylabel("$x[n]$")
        ax[0].grid()
        ax[0].set_ylim([-1.1, 1.1])

        ax[1].plot(t, yt)
        ax[1].plot(xn, linestyle="None", marker="o")
        ax[1].set_xlabel("$t$")
        ax[1].set_ylabel("$y(t)$")
        ax[1].grid()
        ax[1].set_ylim([-1.1, 1.1])
        fig.tight_layout()
        st.pyplot(fig)

    with tab3:
        Rb = 1/Tb
        fa = sps * Rb # Freq de amostragem (samples/s)
        n_bits = 50
        dur = n_bits * Tb
        Na = n_bits * sps # Número de amostras
        f = np.arange(-Na//2 , Na//2) / Na * fa # Eixo da frequencia, obs: // = divisão que gera um inteiro
        yts = []
        for _ in range(1000):
            bn = np.random.randint(0, 2, n_bits)
            xn = mapping(bn)
            yt = pam(xn)
            yts.append(yt)
        Yfs = fftshift(fft(yts)) / sps

        psd_sim = np.mean(np.abs(Yfs)**2/dur, axis = 0) # axis C0luna, L1nha

        fig, ax = plt.subplots()
        ax.plot(f, psd_sim, label="Simulado")
        ax.plot(f, psd_teo(f), label="Teórico")
        ax.set_xlim(-4, 4)
        ax.legend()
        ax.grid()
        st.pyplot(fig)

if __name__ == "__main__":
    main()