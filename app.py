import streamlit as st
import datetime

st.set_page_config(page_title="Policy Summary Prototype", layout="wide")
st.title("📄 Policy Summary Entry Form")

st.markdown("Fill in the fields below exactly like the Excel 'Policy Overview' row")

with st.form("policy_entry_form"):
    st.subheader("Policy Details")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        policy_name = st.text_input("Policy Name")
        policy_no = st.text_input("Policy No")
        company = st.text_input("Company")
        type_of_coverage = st.text_input("Type of coverage")
    
    with col2:
        inception_date = st.date_input("Inception Date", value=datetime.date.today())
        maturity_date = st.date_input("Maturity Date")
        premium_date = st.date_input("Premium Date")
        premium_mode = st.selectbox("Premium Mode", ["Annual", "Semi-Annual", "Quarterly", "Monthly"])

    with col3:
        annual_premium_cpf = st.number_input("Annual Premium CPF", value=0.0)
        annual_premium_cash = st.number_input("Annual Premium CASH", value=0.0)
        premium_years = st.number_input("Premium Paying Years", step=1)
        remark = st.text_input("Remark")

    with col4:
    death = st.number_input("Death (Editable, Blue)", value=0.0)
    major_ci = st.number_input("Major CI (Editable, Orange)", value=0.0)
    early_ci = st.number_input("Early CI (Editable, Purple)", value=0.0)
    cash_value = st.number_input("Cash Value (Editable, Green)", value=0.0)

