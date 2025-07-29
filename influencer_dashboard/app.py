import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Set layout
st.set_page_config(page_title="Influencer Dashboard", layout="wide")

# Load logo
logo = Image.open("logo.png")
st.image(logo, width=150)

# ✅ Inject custom CSS
def load_custom_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css("styles.css")

st.title("📢 Influencer Campaign Performance Dashboard")
st.markdown("**Powered by HealthKart | Intern Project by Bonda Naveen Kumar**")

# Load Data
@st.cache_data
def load_data():
    influencers = pd.read_csv("influencers.csv")
    posts = pd.read_csv("posts.csv")
    tracking = pd.read_csv("tracking_data.csv")
    payouts = pd.read_csv("payouts.csv")
    return influencers, posts, tracking, payouts

influencers, posts, tracking, payouts = load_data()
st.sidebar.header("🔎 Filters")

platforms = st.sidebar.multiselect("Platform", options=tracking['source'].unique(), default=tracking['source'].unique())
products = st.sidebar.multiselect("Product", options=tracking['product'].unique(), default=tracking['product'].unique())
influencer_ids = st.sidebar.multiselect("Influencer", options=influencers['name'], default=influencers['name'])

# Filter data
filtered_tracking = tracking[
    (tracking['source'].isin(platforms)) &
    (tracking['product'].isin(products)) &
    (tracking['influencer_id'].isin(influencers[influencers['name'].isin(influencer_ids)]['id']))
]

# Tabs for layout
tab1, tab2, tab3 = st.tabs(["📊 Overview", "👑 Top Performers", "📂 Upload & Data View"])

# ----------------- TAB 1: KPIs & Revenue by Platform ----------------- #
with tab1:
    st.subheader("📈 Campaign KPIs")

    merged = pd.merge(filtered_tracking, payouts, on="influencer_id")
    total_revenue = filtered_tracking['revenue'].sum()
    total_payout = merged['total_payout'].sum()
    roas = total_revenue / total_payout if total_payout > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("🧾 Total Payout", f"₹{total_payout:,.2f}")
    col3.metric("📊 ROAS", f"{roas:.2f}x")

    st.subheader("🧪 Revenue by Platform")
    revenue_platform = filtered_tracking.groupby('source')['revenue'].sum().reset_index()
    fig1 = px.bar(revenue_platform, x='source', y='revenue', title="Revenue by Platform", color='source')
    st.plotly_chart(fig1, use_container_width=True)

# ----------------- TAB 2: Top Influencers & ROAS ----------------- #
with tab2:
    st.subheader("🏆 Top Influencers by Revenue")

    tracking_named = pd.merge(filtered_tracking, influencers[['id', 'name']], left_on='influencer_id', right_on='id')
    top_influencers = tracking_named.groupby('name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_influencers, x='revenue', y='name', orientation='h', title="Top 10 Influencers by Revenue", color='revenue')
    st.plotly_chart(fig2, use_container_width=True)


    st.subheader("💹 ROAS by Influencer")

    roi_data = filtered_tracking.groupby('influencer_id')['revenue'].sum().reset_index()
    roi_data = roi_data.merge(payouts, on='influencer_id')
    roi_data = roi_data.merge(influencers[['id', 'name', 'followers']], left_on='influencer_id', right_on='id')
    roi_data['ROAS'] = roi_data['revenue'] / roi_data['total_payout']

    fig3 = px.scatter(
        roi_data,
        x='revenue',
        y='ROAS',
        size='followers',
        color='name',
        title="Influencer ROAS Distribution",
        hover_name='name',
        size_max=60
    )
    st.plotly_chart(fig3, use_container_width=True)
# ----------------- TAB 3: Upload & Preview Data ----------------- #
with tab3:
    st.subheader("📤 Upload Custom CSV Data")

    uploaded_influencers = st.file_uploader("Upload influencers.csv", type="csv")
    uploaded_posts = st.file_uploader("Upload posts.csv", type="csv")
    uploaded_tracking = st.file_uploader("Upload tracking_data.csv", type="csv")
    uploaded_payouts = st.file_uploader("Upload payouts.csv", type="csv")

    st.markdown("---")

    # Reload data from uploaded files if all are provided
    if uploaded_influencers and uploaded_posts and uploaded_tracking and uploaded_payouts:
        influencers = pd.read_csv(uploaded_influencers)
        posts = pd.read_csv(uploaded_posts)
        tracking = pd.read_csv(uploaded_tracking)
        payouts = pd.read_csv(uploaded_payouts)
        st.success("✅ Custom datasets successfully loaded!")
    else:
        st.info("ℹ️ Upload all 4 CSV files above to override default data.")

    # Show current dataframes
    st.subheader("📂 Current Data Preview")
    st.markdown("### 👥 Influencers")
    st.dataframe(influencers)

    st.markdown("### 📸 Posts")
    st.dataframe(posts)

    st.markdown("### 📦 Tracking Data")
    st.dataframe(tracking)

    st.markdown("### 💸 Payouts")
    st.dataframe(payouts)
