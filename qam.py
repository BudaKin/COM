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

    bits = source(n_bits)

    x_n = qam.modulate(bits)
    x_t = komm.sampling_rate_expand(x_n, sps) * fa
    p_t = pulse.taps(sps)
    s_t = np.convolve(p_t, x_t) * dt

    t = np.arange(s_t.size) * dt

    s_bp_t = np.real(s_t * np.exp(2j * np.pi * fc *t))

    EbN0_dB_list = np.arange(-10, 11)
    EbN0_list = 10**(EbN0_dB_list/10)

    Pb_teo_list = []
    Pb_sim_list = []
    Es = qam.energy_per_symbol

    for EbN0 in EbN0_list:
        EsN0 = k * EbN0
        Ps = 3 * komm.gaussian_q(np.sqrt(EsN0/5))
        Pb = Ps/k
        Pb_teo_list.append(Pb)
        # Sim
        N0 = Es / EsN0
        z_real = rng.normal(loc=0, scale=np.sqrt(N0/2), size=x_n.size)
        z_imag = rng.normal(loc=0, scale=np.sqrt(N0/2), size=x_n.size)
        z_n = z_real + 1j * z_imag
        y_n = x_n + z_n # AWGN vetorial
        bits_hat = qam.demodulate_hard(y_n)
        Pb = np.mean(bits != bits_hat)
        Pb_sim_list.append(Pb)

    st.title("16-QAM")

    tabs = st.tabs(["Constelação", "Forma de onda", "BER"])

    with tabs[0]:
        fig, ax = plt.subplots()

        ax.plot(y_n.real, y_n.imag, "C1.", alpha=0.1) # type:ignore
        ax.plot(qam.constellation.real, qam.constellation.imag, "C0o")
        ax.set_xlabel("Parte Real")
        ax.set_ylabel("Parte Imag")

        ax.set_aspect("equal")
        ax.grid()
        ax.set_xticks(np.arange(-3, 4, 1))
        st.pyplot(fig)

    with tabs[1]:
        fig, ax = plt.subplots(1, 2)
        n_symb = 5

        ax[0].plot(t[:n_symb*sps], s_t.real[:n_symb*sps], label="Real")
        ax[0].plot(t[:n_symb*sps], s_t.imag[:n_symb*sps], label="Imag")
        ax[0].set_ylabel("$s(t)$")
        ax[0].set_xlabel("$t$")
        ax[0].grid()
        ax[0].set_xticks(np.arange(0, n_symb+1, 1))
        ax[0].legend(loc="upper right")

        ax[1].plot(t[:n_symb*sps], np.abs(s_t)[:n_symb*sps], label="Abs")
        ax[1].plot(t[:n_symb*sps], np.angle(s_t)[:n_symb*sps], label="Angle")
        ax[1].set_ylabel("$s(t)$")
        ax[1].set_xlabel("$t$")
        
        ax[1].grid()
        ax[1].set_xticks(np.arange(0, n_symb+1, 1))
        ax[1].legend(loc="upper right")
        fig.tight_layout()

        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.plot(t[:n_symb*sps], s_bp_t[:n_symb*sps])
        ax.grid()
        ax.set_ylabel("$s(t)$")
        ax.set_xlabel("$t$")
        ax.set_xticks(np.arange(0, n_symb+1, 1))
        st.pyplot(fig)

    with tabs[2]:
        fig, ax = plt.subplots()
        ax.semilogy(EbN0_dB_list, Pb_teo_list, label="Teo")
        ax.semilogy(EbN0_dB_list, Pb_sim_list, label="Sim")
        ax.set_xlabel("$E_b/N_0$")
        ax.set_ylabel("$P_b$")
        ax.grid()
        ax.legend()
        st.pyplot(fig) 

if __name__ == "__main__":
    main()