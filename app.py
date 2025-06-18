import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Policy Summary Table", layout="wide")
st.title("📄 Multi-Policy Summary Table")

# Dropdown values extracted from Excel
coverage_options = [
    "HOSPITALISATION", "CARESHIELD ENHANCEMENT", "PERSONAL ACCIDENT",
    "GROUP TERM ACCIDENT", "WHOLE LIFE PLAN", "INVESTMENT LINKED LIFE PLAN",
    "TERM", "GROUP TERM LIFE", "GROUP TERM CI", "DISABILITY",
    "ENDOWMENT", "INVESTMENT", "CPF INVESTMENT"
]

company_options = [
    "AIA", "PRUDENTIAL", "GREAT EASTERN", "SINGLIFE-AVIVA", "HSBC LIFE",
    "MANULIFE", "TOKIO MARINE", "HL ASSURANCE", "ETIQA", "FWD"
]

# Client DOB input (for age calculation)
st.sidebar.header("Client Info")
dob = st.sidebar.date_input("Client Date of Birth", value=datetime.date(1990, 1, 1))
current_year = datetime.date.today().year
client_age = current_year - dob.year

# Number of policies
num_policies = st.sidebar.number_input("Number of Policies", min_value=1, max_value=20, value=3)

# Policy table
st.markdown("### ✍️ Enter Policy Details")
data = []

for i in range(num_policies):
    st.markdown(f"#### Policy {i + 1}")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        policy_name = st.text_input(f"Policy Name {i}")
        company = st.selectbox(f"Company {i}", company_options)
        type_coverage = st.selectbox(f"Type of Coverage {i}", coverage_options)
        policy_no = st.text_input(f"Policy No {i}")

    with col2:
        incep_date = st.date_input(f"Inception Date {i}", value=datetime.date.today())
        mat_date = st.date_input(f"Maturity Date {i}", value=datetime.date.today())
        premium_cpf = st.number_input(f"CPF Premium {i}", value=0.0)
        premium_cash = st.number_input(f"Cash Premium {i}", value=0.0)

    with col3:
        premium_years = st.number_input(f"Premium Paying Years {i}", value=0)
        premium_mode = st.selectbox(f"Premium Mode {i}", ["Annual", "Semi-Annual", "Quarterly", "Monthly"])
        remark = st.text_input(f"Remark {i}")
        premium_date = st.date_input(f"Premium Date {i}", value=datetime.date.today())

    with col4:
        death = st.number_input(f"Death {i}", value=0.0)
        major_ci = st.number_input(f"Major CI {i}", value=0.0)
        early_ci = st.number_input(f"Early CI {i}", value=0.0)
        cash_value = st.number_input(f"Cash Value {i}", value=0.0)

    # Auto calculate inception and maturity age
    inception_age = incep_date.year - dob.year
    maturity_age = mat_date.year - dob.year

    data.append({
        "Policy Name": policy_name,
        "Policy No": policy_no,
        "Company": company,
        "Type of Coverage": type_coverage,
        "Inception Date": incep_date,
        "Maturity Date": mat_date,
        "Inception Age": inception_age,
        "Maturity Age": maturity_age,
        "CPF Premium": premium_cpf,
        "Cash Premium": premium_cash,
        "Premium Years": premium_years,
        "Premium Mode": premium_mode,
        "Premium Date": premium_date,
        "Death": death,
        "Major CI": major_ci,
        "Early CI": early_ci,
        "Cash Value": cash_value,
        "Remark": remark
    })

if st.button("Submit All Policies"):
    df = pd.DataFrame(data)
    st.success("✅ All policies submitted!")
    st.dataframe(df)

    # Plotting
    st.subheader("📊 Coverage Over Time")
    for coverage_type in ["Death", "Major CI", "Early CI"]:
        fig, ax = plt.subplots()
        ax.bar(df["Inception Age"], df[coverage_type], label=coverage_type)
        ax.set_xlabel("Client Age")
        ax.set_ylabel(f"{coverage_type} Coverage")
        ax.set_title(f"{coverage_type} Coverage by Inception Age")
        st.pyplot(fig)

    # Investment projection (simple example)
    st.subheader("📈 Investment Projection")
    base_invest = 50000  # Static base for demo, can be user input
    annual_return = 0.06
    years = list(range(client_age, 100))
    values = [base_invest * ((1 + annual_return) ** (y - client_age)) for y in years]
    fig2, ax2 = plt.subplots()
    ax2.plot(years, values, label="Investment Value")
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Projected Value")
    ax2.set_title("Investment Returns Over Time")
    st.pyplot(fig2)
