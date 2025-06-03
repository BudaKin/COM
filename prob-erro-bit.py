import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import komm.abc as abc

def main():
    st.title("Probabilidade de erro de bit")
    tab1, tab2 = st.tabs(["Ex1", "Ex2"])
    with tab1:
        Rb = 10e3       # kbits/s
        Tb = 1/Rb       # s
        No = 32e-5      # W/Hz
        A = 2.0         # V
        Eb = A**2 * Tb  # J
        Pb_teo = komm.gaussian_q(np.sqrt(2*Eb/No))

        # Simulação
        n_bits = 10000 # Número de bits
        rng=np.random.default_rng(seed=42)
        dms = komm.DiscreteMemorylessSource(
            pmf=[0.5,0.5],
            rng=rng,
        )

        sps = 100
        pulse = komm.RectangularPulse()
        tx_filter = komm.TransmitFilter(pulse, sps)

        bits = dms(n_bits)

        x_n = 2.0*bits - 1.0 # Polar
        s_t = A*tx_filter(x_n)
        ts, _ = tx_filter.axes(x_n)
        ts *= Tb

        fig, ax = plt.subplots(3, 1, figsize=(6, 5))

        ax[0].plot(ts/1e-6, s_t, color="C0")
        ax[0].set_xlim(0, 10*Tb/1e-6)
        ax[0].set_xlabel("$t$ (µs)")
        ax[0].set_ylabel("$s(t)$ (V)")
        ax[0].set_xticks(np.arange(0, 1001, 100))
        ax[0].grid()

        snr = A**2 / (No/2)
        Ta = Tb/sps
        fa = 1/Ta

        awgn = komm.AWGNChannel(
            signal_power=A**2,
            snr=snr/fa,
            rng=rng,
        )

        r_t = awgn(s_t)

        ax[1].plot(ts/1e-6, r_t, color="C1")
        ax[1].set_xlim(0, 10*Tb/1e-6)
        ax[1].set_xlabel("$t$ (µs)")
        ax[1].set_ylabel("$r(t)$ (V)")
        ax[1].set_xticks(np.arange(0, 1001, 100))
        ax[1].grid()
        fig.tight_layout()

        t = np.arange(0.0, Tb, Ta)
        hr_t = pulse.waveform(Tb - t)

        y_t = np.convolve(hr_t, r_t)/sps
        y_t = y_t[0:s_t.size]

        ax[2].plot(ts/1e-6, y_t, color="C2")
        ax[2].set_xlim(0, 10*Tb/1e-6)
        ax[2].set_xlabel("$t$ (µs)")
        ax[2].set_ylabel("$y(t)$ (V)")
        ax[2].set_xticks(np.arange(0, 1001, 100))
        ax[2].grid()

        y_n = y_t[sps-1::sps] # Amostrador de sps para sps

        bits_hat = (y_n > 0).astype(int) # Decisor

        Pb_sim = np.mean(bits != bits_hat) # BER = Bit error rate

        st.metric("$P_b$ Teórica", f"{Pb_teo:.2%}")
        st.metric("$P_b$ Simulada", f"{Pb_sim:.2%}")

        st.pyplot(fig)


        
    with tab2:
        Pb_teo = 1e-3
        No = 2e-4
        A = 10.0

        Q_inv = komm.gaussian_q_inv(Pb_teo)
        Eb = (Q_inv*np.sqrt(No)/np.sqrt(2))**2
        st.metric("Eb", f"{Eb * 1e6:.2f} µJ")
        Tb = 2*Eb/A**2
        st.metric("Tb", f"{Tb * 1e6:.2f} µs")
        Rb = 1/Tb
        st.metric("Rb", f"{Rb * 1e-3:.2f} kbits/s")
        Pb_teo = komm.gaussian_q(np.sqrt(2*Eb/No))

        # Eb = A**2 * Tb /2 # Valor teste
        # Tb = 19.09e-6  # Valor teste
        # Rb = 1/Tb # Valor teste

        # Simulação
        n_bits = 100000 # Número de bits
        rng=np.random.default_rng(seed=42)
        dms = komm.DiscreteMemorylessSource(
            pmf=[0.5,0.5],
            rng=rng,
        )

        sps = 100
        pulse = komm.RectangularPulse(0.5)
        tx_filter = komm.TransmitFilter(pulse, sps)

        bits = dms(n_bits)

        x_n = 2.0*bits - 1.0 # Polar
        s_t = A*tx_filter(x_n)
        ts, _ = tx_filter.axes(x_n)
        ts *= Tb

        fig, ax = plt.subplots(3, 1, figsize=(6, 5))

        ax[0].plot(ts/1e-6, s_t, color="C0")
        ax[0].set_xlim(0, 10*Tb/1e-6)
        ax[0].set_xlabel("$t$ (µs)")
        ax[0].set_ylabel("$s(t)$ (V)")
        # ax[0].set_xticks(np.arange(0, 1001, 100))
        ax[0].grid()

        signal_power = A**2 / 2
        snr = signal_power / (No/2)
        Ta = Tb/sps
        fa = 1/Ta

        awgn = komm.AWGNChannel(
            signal_power=signal_power,
            snr=snr/fa,
            rng=rng,
        )

        r_t = awgn(s_t)

        ax[1].plot(ts/1e-6, r_t, color="C1")
        ax[1].set_xlim(0, 10*Tb/1e-6)
        ax[1].set_xlabel("$t$ (µs)")
        ax[1].set_ylabel("$r(t)$ (V)")
        ax[1].set_xticks(np.arange(0, 1001, 100))
        ax[1].grid()
        fig.tight_layout()

        t = np.arange(0.0, Tb, Ta)
        hr_t = pulse.waveform(1 - t/Tb)

        y_t = np.convolve(hr_t, r_t)/sps
        y_t = y_t[0:s_t.size]

        ax[2].plot(ts/1e-6, y_t, color="C2")
        ax[2].set_xlim(0, 10*Tb/1e-6)
        ax[2].set_xlabel("$t$ (µs)")
        ax[2].set_ylabel("$y(t)$ (V)")
        ax[2].set_xticks(np.arange(0, 1001, 100))
        ax[2].grid()

        y_n = y_t[sps-1::sps] # Amostrador de sps para sps

        bits_hat = (y_n > 0).astype(int) # Decisor

        Pb_sim = np.mean(bits != bits_hat) # BER = Bit error rate

        st.metric("$P_b$ Teórica", f"{Pb_teo:.2%}")
        st.metric("$P_b$ Simulada", f"{Pb_sim:.2%}")

        st.pyplot(fig)


if __name__ == "__main__":
    main()