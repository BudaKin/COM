import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import komm.abc as abc
from numpy.fft import fft, fftshift

st.title("Diagrana de olho")

rolloff = st.slider(
    label="Fator de rollof $\\alpha:",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
)

pulse = komm.RaisedCosinePulse(rolloff)

tabs = st.tabs(["Pulso", "Sinal", "🧿"])

with tabs[0]:
    fig, ax = plt.subplots(1, 2, figsize=(12,4))

    ts = np.linspace(-8, 8, num=1000)
    tempo = ax[0]
    tempo.plot(ts, pulse.waveform(ts))
    tempo.set_ylim(-0.25, 1.25)
    tempo.grid()
    tempo.set_xlabel("$t$")
    tempo.set_xlabel("$p(t)$")

    fs = np.linspace(-1.5, 1.5, num=1000)
    freq = ax[1]
    freq.plot(fs, pulse.spectrum(fs))
    freq.set_ylim(-0.25, 1.25)
    freq.grid()
    freq.set_xlabel("$f$")
    freq.set_xlabel("$P(f)$")
    fig.tight_layout()
    st.pyplot(fig)
    pass
with tabs[1]:
    sps = 20
    rng = np.random.default_rng(seed=7)
    source = komm.DiscreteMemorylessSource(
        [0.5, 0.5], rng
    )
    bits = source(1000)
    x = 2.0*bits - 1.0

    tx_filter = komm.TransmitFilter(
        pulse, sps, truncation=32
    )

    y = tx_filter(x)

    fig, ax = plt.subplots(figsize=(6,3))
    ts, _ = tx_filter.axes(x)
    ns = np.arange(31)
    ax.plot(ts, y)
    ax.plot(ns, x[:31], 'o')
    ax.grid()
    ax.set_xlabel("$t$")
    ax.set_xlabel("$y(t)$")
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlim(-10, 30)
    st.pyplot(fig)

with tabs[2]:
    fig, ax = plt.subplots(figsize=(6,3))
    span = 3
    samples_per_span = span * sps
    for i in range(10, bits.size // span):
        ts = np.linspace(
                        start=0, 
                        stop=span, 
                        num=samples_per_span, 
                        endpoint=False,
        )

        ax.plot(
            ts, 
            y[samples_per_span*i:samples_per_span*(i+1)],
            "C2",
            alpha=0.25
        )
    ax.set_ylim(-2.5, 2.5)
    ax.grid()
    st.pyplot(fig)