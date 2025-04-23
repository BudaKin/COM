import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import komm.abc as abc

def main():
    pulse_menu = {
        "Retangular NRZ" : komm.RectangularPulse(1),
        "Retangular RZ" : komm.RectangularPulse(0.5),
        "Manchester" : komm.ManchesterPulse(),
    }
    st.title("Códigos de Linha")
    pulse_choice = st.segmented_control(
        label="Pulso:",
        options=pulse_menu.keys(),
        default="Retangular NRZ",
    )
    if pulse_choice is None:
        raise Exception("Nenhum Pulso escolhido.")
    pulse: abc.Pulse = pulse_menu[pulse_choice]
    tab1, tab2 = st.tabs(["Pulso", "Sinal"])
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
    bn = np.random.randint(0, 2, size=Nbits)
    st.write(f"Bits: {bn}")
    sps = 100 # Samples per symbol
    pam = komm.TransmitFilter(pulse, sps)
    xn = 2*bn - 1
    yt = pam(bn)
    t = pam.time(bn)

    with tab2:
        fig, ax = plt.subplots(2,1)
        ax[0].stem(xn)
        ax[0].set_xlabel("$n$")
        ax[0].set_ylabel("$x[n]$")
        ax[0].grid()
        ax[0].set_xlim([-1, 7])

        ax[1].plot(t, yt)
        ax[1].plot(xn, linestyle="None", marker="o")
        ax[1].set_xlabel("$t$")
        ax[1].set_ylabel("$y(t)$")
        ax[1].grid()
        ax[1].set_xlim([-1, 7])
        fig.tight_layout()
        st.pyplot(fig)
    

if __name__ == "__main__":
    main()