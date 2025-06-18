# Full-featured Streamlit App with Multiple Policies, Withdrawals & Download Option

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# --- PAGE SETUP ---
st.set_page_config(page_title="Retirement Portfolio Planner", layout="wide")
st.title("📊 Retirement & Insurance Portfolio Planner")
st.markdown("Use this tool to model CPF, investment, and insurance projections with withdrawals and downloadable summary.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Client Info")
client_name = st.sidebar.text_input("Client Name", "John Doe")
current_age = st.sidebar.number_input("Current Age", 0, 100, 35)
retirement_age = st.sidebar.number_input("Retirement Age", current_age, 100, 65)
end_age = st.sidebar.number_input("Projection End Age", retirement_age, 100, 85)

# CPF Info
st.sidebar.header("CPF Info")
cpf_balance = st.sidebar.number_input("Current CPF Balance", 0, 10**7, 100000)
cpf_return = st.sidebar.slider("CPF Annual Return (%)", 0.0, 6.0, 4.0)

# Investment Info
st.sidebar.header("Investment Info")
inv_balance = st.sidebar.number_input("Investment Current Value", 0, 10**7, 50000)
inv_return = st.sidebar.slider("Investment Annual Return (%)", 0.0, 12.0, 6.0)

# Insurance Policies
st.sidebar.header("Insurance Policies")
num_policies = st.sidebar.number_input("Number of Policies", 0, 5, 2)
policies = []

for i in range(num_policies):
    st.sidebar.markdown(f"**Policy {i+1}**")
    payout = st.sidebar.number_input(f"P{i+1} Annual Payout", 0, 500000, 10000, key=f"payout{i}")
    payout_start = st.sidebar.number_input(f"P{i+1} Start Age", current_age, 100, retirement_age, key=f"start{i}")
    payout_end = st.sidebar.number_input(f"P{i+1} End Age", payout_start, 100, end_age, key=f"end{i}")
    policies.append({"payout": payout, "start": payout_start, "end": payout_end})

# Withdrawal Strategy
st.sidebar.header("Withdrawal Strategy")
withdraw_cpf = st.sidebar.checkbox("Withdraw from CPF after retirement", True)
withdraw_inv = st.sidebar.checkbox("Withdraw from Investments after retirement", True)
withdraw_amount = st.sidebar.number_input("Annual Withdrawal Amount (each source)", 0, 100000, 12000)

# --- CALCULATION ---
ages = list(range(current_age, end_age + 1))
years = len(ages)

# CPF and Investment Growth Projections
cpf_vals, inv_vals = [cpf_balance], [inv_balance]
for i in range(1, years):
    prev_cpf = cpf_vals[-1] * (1 + cpf_return / 100)
    prev_inv = inv_vals[-1] * (1 + inv_return / 100)

    age = ages[i]
    if withdraw_cpf and age >= retirement_age:
        prev_cpf -= withdraw_amount
    if withdraw_inv and age >= retirement_age:
        prev_inv -= withdraw_amount

    cpf_vals.append(max(prev_cpf, 0))
    inv_vals.append(max(prev_inv, 0))

# Insurance Income
insurance_income = []
for age in ages:
    total = 0
    for pol in policies:
        if pol['start'] <= age <= pol['end']:
            total += pol['payout']
    insurance_income.append(total)

# Retirement Income Calculation
cpf_income = [0] + list(np.diff(cpf_vals))
inv_income = [0] + list(np.diff(inv_vals))
total_income = [c + i + ins for c, i, ins in zip(cpf_income, inv_income, insurance_income)]

# --- TABLE ---
df = pd.DataFrame({
    "Age": ages,
    "CPF Value": cpf_vals,
    "Investment Value": inv_vals,
    "Annual Insurance Income": insurance_income,
    "CPF Income": cpf_income,
    "Investment Income": inv_income,
    "Total Retirement Income": total_income
})

# --- DISPLAY TABLE & CHARTS ---
st.subheader(f"📋 Projection Table for {client_name}")
st.dataframe(df.style.format({
    "CPF Value": "S$ {:,.0f}",
    "Investment Value": "S$ {:,.0f}",
    "Annual Insurance Income": "S$ {:,.0f}",
    "CPF Income": "S$ {:,.0f}",
    "Investment Income": "S$ {:,.0f}",
    "Total Retirement Income": "S$ {:,.0f}"
}), use_container_width=True)

# Charts
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Portfolio Value Over Time")
    fig, ax = plt.subplots()
    ax.plot(ages, cpf_vals, label="CPF Value")
    ax.plot(ages, inv_vals, label="Investment Value")
    ax.set_xlabel("Age")
    ax.set_ylabel("Value (SGD)")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("💰 Annual Retirement Income")
    fig2, ax2 = plt.subplots()
    ax2.plot(ages, total_income, label="Total Income", color='green')
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Income (SGD)")
    ax2.legend()
    st.pyplot(fig2)

# --- DOWNLOAD ---
st.subheader("⬇️ Download Summary")
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Projection')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(df)
st.download_button("Download Excel Report", data=excel_data, file_name="portfolio_summary.xlsx")
