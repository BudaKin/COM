import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import komm
import komm.abc

# st.set_page_config(layout="wide")

st.title("Filtro Casado")

pulse_menu = {
        "NRZ" : komm.RectangularPulse(1),
        "RZ" : komm.RectangularPulse(0.5),
        "Manch" : komm.ManchesterPulse(),
        "Sinc" : komm.SincPulse(),
        "RC" : komm.RaisedCosinePulse(0.5),
}

cols = st.columns(3)
with cols[0]:
    tx_pulse_choice = st.segmented_control(
        label="TX pulse:",
        options=pulse_menu.keys(),
        key=0,
    )
    tx_pulse = komm.abc.Pulse
    if tx_pulse_choice is None:
        raise Exception("Escolha um pulso")
    tx_pulse = pulse_menu[tx_pulse_choice]

with cols[1]:
    rx_pulse_choice = st.segmented_control(
        label="RX pulse:",
        options=pulse_menu.keys(),
        key=1,
    )
    rx_pulse = komm.abc.Pulse | None
    if rx_pulse_choice is None:
        rx_pulse = None 
    else:
        rx_pulse = pulse_menu[rx_pulse_choice]

with cols[2]:
    channel_snr_db = st.slider(
        "Channel_SNR (dB):",
        min_value=-1,
        max_value=40,
        value=30,
    )

channel_snr = 10**(channel_snr_db/10)
rng = np.random.default_rng(seed=42)

n_bits = 500
sps = 100
dms = komm.DiscreteMemorylessSource([0.5, 0.5], rng=rng)
tx_filter = komm.TransmitFilter(tx_pulse, sps)

bits = dms(n_bits)
x_n = 2*bits - 1 # Polar

s_t = tx_filter(x_n)
t, _ = tx_filter.axes(x_n)

awgn = komm.AWGNChannel(
    signal_power=1.0, # TODO: handle RZ case
    snr=channel_snr,
    rng=rng,
)
r_t = awgn(s_t)

tab1, tab2 = st.tabs(["Sinais", "Olho"])

with tab1:
    fig, ax = plt.subplots(3,1)
    ax[0].plot(t, s_t, color="C0")
    ax[0].grid()
    ax[0].set_xlim(0, 20)
    ax[0].set_ylim(-2, 2)
    ax[0].set_xticks(range(21))
    ax[0].set_xlabel("t")
    ax[0].set_ylabel("$s(t)$")

    ax[1].plot(t, r_t, color="C1")
    ax[1].grid()
    ax[1].set_xlim(0, 20)
    ax[1].set_ylim(-2, 2)
    ax[1].set_xticks(range(21))
    ax[1].set_xlabel("t")
    ax[1].set_ylabel("$r(t)$")

    fig.tight_layout()
    st.pyplot(fig)

with tab2:
    pass