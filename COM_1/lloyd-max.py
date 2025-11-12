from math import sqrt, pi, exp
from typing import Callable
import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def gaussian(x: float) -> float:
    return 1 / sqrt(2*pi) * exp(-x**2/2)

def uniform(x: float) -> float:
    return 0.1 if -5 <= x <= 5 else 0

def laplacian(x: float) -> float:
    return 0.5*exp(-abs(x))

def gaussian_mixture(x: float) -> float:
    return (0.25 * (1/0.5) * gaussian((x+3)/0.5) + 0.75 * (1/0.8) * gaussian((x-2)/0.8))

def valor_esperado_condicionado(
        pdf: Callable[[float], float],
        xi: float, # inicial
        xf: float, # final
) -> float:
    xs = np.linspace(xi, xf, 1000)
    num = np.trapezoid([x * pdf(x) for x in xs], xs)
    deno = np.trapezoid([pdf(x) for x in xs], xs)
    return num/deno # type: ignore

def lloyd_max_step(
        pdf: Callable[[float], float],
        a: float, 
        b:float, 
        L: int,
        vs: list[float]
):
    # Níveis -> limiares
    ls = [0.0] * (L + 1)
    ls[0] = a
    ls[L] = b
    for i in range(1, L):
        ls[i] = (vs[i - 1] + vs[i])/2
    # Limiares -> Níveis
    new_vs = [0.0] * L
    for i in range(L):
        new_vs[i] = valor_esperado_condicionado(pdf, ls[i], ls[i+1])
    return new_vs, ls

def main():
    st.title("Algoritmo de Lloyd-max")
    col1,col2 = st.columns(2)
    with col1:
        L = st.slider("Número de níveis", 
                    min_value=2,
                    max_value=20,
                    value=4
        )
    with col2:
        pdf_control = st.segmented_control(
            label="PDF",
            options= ["Uniform", "Gaussian", "Laplacian", "Gaussian mixture"],
            default= "Uniform",
        )
        if pdf_control == "Uniform":
            pdf = uniform
        elif pdf_control == "Gaussian":
            pdf = gaussian
        elif pdf_control == "Laplacian":
            pdf = laplacian
        elif pdf_control == "Gaussian mixture":
            pdf = gaussian_mixture
        else:
            raise(ValueError)
        
    a, b = -5, 5
    vss: list[list[float]] = []
    lss: list[list[float]] = []

    vss.append(list(np.linspace(a, b, L))) # Palpite inicial
    for i in range(60):
        vs, ls = lloyd_max_step(pdf,a,b,L,vss[i])
        vss.append(vs)
        lss.append(ls)
    
    tab1, tab2, tab3 = st.tabs(["PDF","Passo-a-passo","MSQE"])

    with tab1:
        fig, ax = plt.subplots()
        fig.set_figheight(4)
        xs = np.linspace(-6, 6, 1000)
        ax.plot(xs, [pdf(x) for x in xs])
        for l in lss[-1]:
            ax.axvline(l, color="C2", linestyle="--")
        ax.set_xlabel("$m$")
        ax.set_ylabel("$f(m)$")
        ax.set_ylim(-0.05, 0.55)
        ax.grid()
        st.pyplot(fig)
    with tab2:
        fig, ax = plt.subplots()

        for i in range(60):
            ax.plot(
                lss[i], 
                [-i] * (L + 1),
                linestyle = "None",
                marker = "|",
                color = "C2"
            )
            ax.plot(
                vss[i], 
                [-i] * L,
                linestyle = "None",
                marker = "o",
                color = "C0"
            )
        
        st.pyplot(fig)
    with tab3:
        pass


if __name__ == "__main__":
    main()
