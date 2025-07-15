import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import komm
import komm.abc

def main():
    rng = np.random.default_rng(seed=128)
    komm.global_rng.set(rng)

    n_bits = 100_000
    Rs = 1.0  # baud = symbols/second
    Ts = 1 / Rs #  second
    sps = 500  # samples/symbol
    fa = Rs * sps  # samples/second
    dt = 1 / fa # second
    fc = 4.0 # hertz
    M = 16
    k = int(np.log2(M))

    source = komm.DiscreteMemorylessSource(2)
    qam = komm.QAModulation(M)
    pulse = komm.RectangularPulse()

    st.title("16-QAM")

    tabs = st.tabs(["Constelação", "Forma de onda", "BER"])

    with tabs[0]:
        fig, ax = plt.subplots()

        ax.plot(qam.constellation.real, qam.constellation.imag, "C0o")
        ax.set_aspect("equal")
        ax.grid()
        ax.set_xticks(np.arange(-3, 4, 1))
        st.pyplot(fig)

    bits = source(n_bits)

    x_n = qam.modulate(bits)
    x_t = komm.sampling_rate_expand(x_n, sps) * fa
    p_t = pulse.taps(sps)
    s_t = np.convolve(p_t, x_t) * dt

    t = np.arange(s_t.size) * dt

    s_bp_t = np.real(s_t * np.exp(2j * np.pi * fc *t))


    with tabs[1]:
        fig, ax = plt.subplots(1, 2)
        n_symb = 5

        ax[0].plot(t[:n_symb*sps], s_t.real[:n_symb*sps], label="Real")
        ax[0].plot(t[:n_symb*sps], s_t.imag[:n_symb*sps], label="Imag")
        ax[0].grid()
        ax[0].set_xticks(np.arange(0, n_symb+1, 1))
        ax[0].legend(loc="upper right")

        ax[1].plot(t[:n_symb*sps], np.abs(s_t)[:n_symb*sps], label="Abs")
        ax[1].plot(t[:n_symb*sps], np.angle(s_t)[:n_symb*sps], label="Angle")
        
        ax[1].grid()
        ax[1].set_xticks(np.arange(0, n_symb+1, 1))
        ax[1].legend(loc="upper right")

        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.plot(t[:n_symb*sps], s_bp_t[:n_symb*sps])
        ax.grid()
        ax.set_xticks(np.arange(0, n_symb+1, 1))
        st.pyplot(fig)

    with tabs[2]:
        fig, ax = plt.subplots(1, 2)
        st.pyplot(fig) 

if __name__ == "__main__":
    main()