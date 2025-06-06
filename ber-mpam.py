import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import komm.abc as abc

def main():
    st.title("$M$-PAM BER")
    rng = np.random.default_rng(seed=42)
    cols = st.columns(2)
    with cols[0]:
        M = st.select_slider(
            label="Ordem da modulação (M)",
            options=[2, 4, 8, 16],
        )
    with cols[1]:
        labeling = st.selectbox(
                    "Mapeamento",
                    ["reflected", "natural"],
        )
    mod = komm.PAModulation(M, labeling=labeling) # reflected = Gray, "natural" = binário padrão
    k = mod.bits_per_symbol
    n_symbs = 20000                     # Número de símbolos transmitidos
    n_bits = n_symbs*k                  # Número de bits transmitidos
    Rs = 40e3                           # Taxa de símbolos (baud)
    Rb =  k * Rs                        # Taxa de bits (bits/s)
    Ts = 1 / Rs                         # Intervalo de símbolos
    A =  4.0                            # Amplitude base do pulso (V)
    Es = A ** 2 * Ts * (M**2 - 1) / 3   # Energia de símbolo (J "=" V²s)  
    Eb = Es / k                         # Energia de bit (J "=" V²s)       

    sps = 100                           # Amostras por símbolo
    fa = sps * Rs                       # Taxa de amostragem (amostras/s)
    Ta = 1 / fa                         # Intervalo de amostragem (s)

    dms = komm.DiscreteMemorylessSource([0.5, 0.5], rng)
    pulse = komm.RectangularPulse()
    tx_filter = komm.TransmitFilter(pulse, sps)

    EbNo_dB_list = np.arange(-8+M//4, 8+M//4 + 1)
    EbNo_list = 10**(EbNo_dB_list/10)

    bits = dms(n_bits)
    x_n = mod.modulate(bits)   
    s_t = A * tx_filter(x_n)
    ts, _ = tx_filter.axes(x_n)

    ts *= Ts

    # BER Teórica
    Pb_teo_list = []
    for EbNo in EbNo_list:
        EsNo = k * EbNo
        Ps = 2 * (M - 1)/ M * \
            komm.gaussian_q(np.sqrt(6/(M**2 - 1) * EsNo))
        Pb = Ps / k
        Pb_teo_list.append(Pb)

    # BER Simulada
    Pb_sim_list = []
    for EbNo in EbNo_list:
        signal_power = Es*Rs
        No = Eb / EbNo
        noise_power = (No/2) * fa
        snr = signal_power/noise_power
        awgn = komm.AWGNChannel(signal_power, snr, rng)
        r_t = awgn(s_t)

        t = np.arange(0.0, Ts, Ta)
        hr_t = pulse.waveform(Ts - t)

        y_t = np.convolve(hr_t, r_t)/sps
        y_t = y_t[0:s_t.size]
        y_n = y_t[sps-1::sps] # Amostrador de sps para sps
        # y_n /= A # Normalização

        bits_hat = mod.demodulate_hard(y_n/A)
        Pb = np.mean(bits_hat != bits)
        Pb_sim_list.append(Pb)
        

    

    tabs = st.tabs(["Sinais", "BER"])
    with tabs[0]:
        fig, ax = plt.subplots(2, 1, figsize=(6,4))
        ax[0].plot(ts/1e-6, s_t)

        ax[0].set_xlim(0, 10*Ts/1e-6)
        ax[0].set_xticks(np.arange(11)*Ts/1e-6)
        ax[0].set_xlabel("$t$ (µs)")

        ax[0].set_yticks(A*np.arange(-(M-1), M, 2))
        ax[0].set_ylabel("$s(t)$")
        ax[0].grid()

        ax[1].plot(ts/1e-6, y_t) # type: ignore

        ax[1].set_xlim(0, 10*Ts/1e-6)
        ax[1].set_xticks(np.arange(11)*Ts/1e-6)
        ax[1].set_xlabel("$t$ (µs)")

        ax[1].set_yticks(A*np.arange(-(M-1), M, 2))
        ax[1].set_ylabel("$y(t)$")
        ax[1].grid()

        fig.tight_layout()
        st.pyplot(fig)
    with tabs[1]:
        fig, ax = plt.subplots(figsize=(6,4))
        # ax.plot(EbNo_list, Pb_list)
        ax.semilogy(EbNo_dB_list, Pb_teo_list, label="Teórico (Gray aprox.)")
        ax.semilogy(EbNo_dB_list, Pb_sim_list, label="simulado")
        ax.set_xlabel("$E_b/N_0$ (dB)")
        ax.set_ylabel("$P_b$")
        ax.legend()
        ax.grid()
        fig.tight_layout()
        st.pyplot(fig)





if __name__ == "__main__":
    main()