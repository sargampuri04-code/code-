import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="YouTube Shorts Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("YouTube_Data.csv")
    return df

df = load_data()

# Title Section
st.title("📊 YouTube Shorts Engagement Dashboard")
st.markdown("""
This dashboard visualizes insights from the YouTube Shorts dataset — including views, engagement rate, likes, and comments.
""")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
channels = st.sidebar.multiselect("Select Channels", sorted(df['Channel_Name'].dropna().unique()), [])
min_views = st.sidebar.number_input("Minimum Views", min_value=0, value=0)
max_age = st.sidebar.number_input("Maximum Age (Days)", min_value=0, value=int(df['Age_In_Days'].max()))

filtered_df = df.copy()
if channels:
    filtered_df = filtered_df[filtered_df['Channel_Name'].isin(channels)]
filtered_df = filtered_df[(filtered_df['Views'] >= min_views) & (filtered_df['Age_In_Days'] <= max_age)]

# KPI Cards
st.subheader("📈 Key Metrics")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Views", f"{filtered_df['Views'].sum():,.0f}")
with c2:
    st.metric("Average Engagement Rate (%)", f"{filtered_df['Engagement_Rate_%'].mean():.2f}")
with c3:
    st.metric("Average Likes", f"{filtered_df['Likes'].mean():,.0f}")
with c4:
    st.metric("Average Comments", f"{filtered_df['Comments'].mean():,.0f}")

# Visualizations
st.subheader("📊 Analytics Visualizations")

tab1, tab2, tab3 = st.tabs(["Views & Engagement", "Likes vs Comments", "Top Channels"])

# Plot 1
with tab1:
    st.markdown("### Views vs Engagement Rate")
    fig1 = px.scatter(
        filtered_df,
        x="Views",
        y="Engagement_Rate_%",
        color="Channel_Name",
        size="Likes",
        hover_data=["Title", "Comments"],
        title="Engagement Rate vs Views",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Plot 2
with tab2:
    st.markdown("### Likes vs Comments Distribution")
    fig2 = px.scatter(
        filtered_df,
        x="Likes",
        y="Comments",
        color="Channel_Name",
        hover_data=["Views", "Engagement_Rate_%"],
        title="Likes vs Comments by Channel",
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Plot 3
with tab3:
    st.markdown("### Top 10 Channels by Average Views")
    top_channels = (
        filtered_df.groupby("Channel_Name")["Views"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig3 = px.bar(
        top_channels,
        x="Channel_Name",
        y="Views",
        text_auto=".2s",
        color="Channel_Name",
        title="Top Channels by Average Views",
        template="plotly_white"
    )
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

# Data Table
st.subheader("📋 Data Preview")
st.dataframe(filtered_df.head(50))

st.markdown("---")
st.caption("© 2026 YouTube Shorts Data Dashboard | Built with Streamlit & Plotly")
