import streamlit as st
import pandas as pd

def calculate_cohen_coon_p(K, tau, theta):
    """Calculate Kc for a P controller using Cohen-Coon tuning rules."""
    Kc = (1 / K) * (tau / theta) * (1 + theta / (3 * tau))
    return Kc

def calculate_cohen_coon_pi(K, tau, theta):
    """Calculate Kc and tau_I for a PI controller using Cohen-Coon tuning rules."""
    Kc = (1 / K) * (tau / theta) * (0.9 + theta / (12 * tau))
    tau_I = theta * (30 + 3 * (theta / tau)) / (9 + 20 * (theta / tau))
    return Kc, tau_I

def calculate_cohen_coon_pid(K, tau, theta):
    """Calculate Kc, tau_I, and tau_D for a PID controller using Cohen-Coon tuning rules."""
    Kc = (1 / K) * (tau / theta) * (4 / 3 + theta / (4 * tau))
    tau_I = theta * (32 + 6 * (theta / tau)) / (13 + 8 * (theta / tau))
    tau_D = theta * (4 / (11 + 2 * (theta / tau)))
    return Kc, tau_I, tau_D

def main():
    st.title("Online Calculator for Cohen-Coon Tuning Parameters based on FOPTD model")

    # Input panel on the left
    with st.sidebar:
        st.header("Input Parameters")
        K = st.number_input("Process Gain (K):", min_value=0.0, value=1.0)
        tau = st.number_input("Time Constant (τ):", min_value=0.0, value=1.0)
        theta = st.number_input("Time Delay (θ):", min_value=0.0, value=0.1, format="%.3f")

        controller_type = st.selectbox("Controller Type:", ["P", "PI", "PID"], index=0)

    # Perform calculation based on controller type
    if controller_type == "P":
        Kc = calculate_cohen_coon_p(K, tau, theta)
        tau_I, tau_D = None, None
    elif controller_type == "PI":
        Kc, tau_I = calculate_cohen_coon_pi(K, tau, theta)
        tau_D = None  # Not applicable for PI controller
    elif controller_type == "PID":
        Kc, tau_I, tau_D = calculate_cohen_coon_pid(K, tau, theta)

    # Prepare results in a table
    data = {
        "Parameter": ["Controller Type", "Controller Gain (Kc)", "Integral Time (τ_I)", "Derivative Time (τ_D)"],
        "Value": [
            controller_type,
            f"{Kc:.4f}",
            f"{tau_I:.4f}" if tau_I is not None else "Not applicable",
            f"{tau_D:.4f}" if tau_D is not None else "Not applicable",
        ],
    }
    df = pd.DataFrame(data)

    # Display results
    st.header("Calculated Parameters")
    st.table(df)

if __name__ == "__main__":
    main()
