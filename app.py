import streamlit as st
import pandas as pd

def score_lead(lead, target_roles, target_industries, min_company_size, role_weight, industry_weight, company_weight):
    score = 0
    if any(role.lower() in lead['Role'].lower() for role in target_roles):
        score += role_weight
    if lead['Industry'] in target_industries:
        score += industry_weight
    if int(lead['Company_Size']) >= min_company_size:
        score += company_weight
    return score

st.set_page_config(page_title="Lead Scoring Dashboard", layout="wide")

st.title("Lead Scoring Dashboard")
st.write("Upload your CSV of leads to get a ranked list of high-quality prospects.")

st.sidebar.header("Lead Scoring Settings")

target_roles = st.sidebar.text_input("Target Roles (comma-separated)", "Manager,Director").split(",")
target_roles = [role.strip() for role in target_roles]

target_industries = st.sidebar.text_input("Target Industries (comma-separated)", "Technology,Finance").split(",")
target_industries = [industry.strip() for industry in target_industries]

min_company_size = st.sidebar.number_input("Minimum Company Size", min_value=1, value=100)

role_weight = st.sidebar.slider("Role Weight", 0, 10, 5)
industry_weight = st.sidebar.slider("Industry Weight", 0, 10, 3)
company_weight = st.sidebar.slider("Company Size Weight", 0, 10, 2)

min_score_filter = st.sidebar.slider("Minimum Score Filter", 0, 20, 0)

uploaded_file = st.file_uploader("Upload leads CSV", type="csv")

if uploaded_file:
    leads = pd.read_csv(uploaded_file)
    leads['Score'] = leads.apply(lambda x: score_lead(x, target_roles, target_industries, min_company_size, role_weight, industry_weight, company_weight), axis=1)
    ranked_leads = leads.sort_values(by='Score', ascending=False)
    filtered_leads = ranked_leads[ranked_leads['Score'] >= min_score_filter]
    
    st.subheader("Top 10 Leads")
    top_leads = filtered_leads.head(10)
    st.dataframe(top_leads.style.highlight_max(subset=['Score'], color='lightgreen'))
    
    st.subheader("All Filtered Leads")
    st.dataframe(filtered_leads)
    
    st.subheader("Lead Distribution by Industry")
    st.bar_chart(filtered_leads['Industry'].value_counts())
    
    st.download_button("Download All Filtered Leads", filtered_leads.to_csv(index=False).encode('utf-8'), "filtered_leads.csv")
    st.download_button("Download Top 10 Leads", top_leads.to_csv(index=False).encode('utf-8'), "top_10_leads.csv")
else:
    st.info("Please upload a CSV file to see scored leads.")