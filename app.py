import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("Chue Myat Noe_Personal Story Dataset.csv")

# Clean columns
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
df['Annual Avg Salary (MMK)'] = pd.to_numeric(df['Annual Avg Salary (MMK)'].str.replace("~","").str.replace(",",""), errors='coerce')
df['Cumulative Salary Growth (MMK)'] = pd.to_numeric(df['Cumulative Salary Growth (MMK)'].str.replace(",",""), errors='coerce')
df['Duration (Months)'] = pd.to_numeric(df['Duration (Months)'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filters")
journey_filter = st.sidebar.multiselect("Journey Type", df['Journey Type'].unique(), default=df['Journey Type'].unique())
year_filter = st.sidebar.multiselect("Year", df['Year'].unique(), default=df['Year'].unique())

filtered_df = df[(df['Journey Type'].isin(journey_filter)) & (df['Year'].isin(year_filter))]

# 0. Headline KPI Row
st.header("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

# Total Roles
total_roles = len(filtered_df)
col1.metric("Total Roles", total_roles)

# Total Volunteer Months
volunteer_months = filtered_df[filtered_df['Journey Type']=="Volunteer"]['Duration (Months)'].sum(skipna=True)
col2.metric("Volunteer Months", int(volunteer_months))

# Current Salary (latest role)
current_salary = filtered_df.dropna(subset=["Annual Avg Salary (MMK)"]).iloc[-1]["Annual Avg Salary (MMK)"]
col3.metric("Current Salary (MMK)", f"{int(current_salary):,}")

# Cumulative Salary Growth
cumulative_salary = filtered_df['Cumulative Salary Growth (MMK)'].max()
col4.metric("Cumulative Salary Growth (MMK)", f"{int(cumulative_salary):,}")

# Longest Role Duration
longest_duration = filtered_df['Duration (Months)'].max()
col5.metric("Longest Role Duration (Months)", int(longest_duration))

# 1. Story Overview
st.title("📖 My Growth Journey Dashboard")
st.write("This dashboard transforms my personal story into structured data, showing how volunteering shaped my career growth.")

# 2. Visualizations
st.header("📊 Data Visualizations")

# Volunteer Journey Timeline Bar Chart
st.subheader("📅 Volunteering Journey Timeline")

# Filter volunteer data only
volunteer_df = filtered_df[filtered_df['Journey Type'] == "Volunteer"]

# Count volunteer activities by year
volunteer_years = volunteer_df.groupby("Year").size().reset_index(name="Number of Volunteer Roles")

# Create bar chart
fig_timeline = px.bar(
    volunteer_years,
    x="Year",
    y="Number of Volunteer Roles",
    text="Number of Volunteer Roles",
    color="Number of Volunteer Roles",
    title="Volunteer Journey Across Years"
)

# Improve layout
fig_timeline.update_layout(
    xaxis_title="Year",
    yaxis_title="Volunteer Activities",
    showlegend=False
)

# Show chart
st.plotly_chart(fig_timeline, use_container_width=True)

# Salary growth line
fig_salary = px.line(filtered_df.dropna(subset=["Cumulative Salary Growth (MMK)"]),
                     x="Year", y="Cumulative Salary Growth (MMK)", markers=True)
st.subheader("Cumulative Salary Growth Over Time")
st.plotly_chart(fig_salary, use_container_width=True)

# Role distribution bar
fig_roles = px.histogram(filtered_df, x="Journey Type", color="Journey Type")
st.subheader("Volunteer vs Employment Roles")
st.plotly_chart(fig_roles, use_container_width=True)

# Volunteer duration heatmap
fig_volunteer = px.density_heatmap(filtered_df[filtered_df['Journey Type']=="Volunteer"],
                                   x="Year", y="Duration (Months)", color_continuous_scale="Blues")
st.subheader("Volunteer Duration Heatmap")
st.plotly_chart(fig_volunteer, use_container_width=True)

# 3. Key Insights
st.header("🔍 Key Insights")
st.write("""
- Volunteering built leadership and HR skills before paid employment.
- Salary growth accelerated in 2022, 2024, and 2026.
- Civic engagement remained consistent across years.
""")

# 4. Decision-Making Section
st.header("🎯 Decision-Making")
st.write("""
Based on the data:
- Continue combining volunteering with career roles.
- Focus on HR and customer success pathways.
- Negotiate salary proactively at career transitions.
""")

# 5. Ethics & Responsibility
st.header("⚖️ Ethics & Responsibility")
st.write("""
- **Privacy Statement**: Dataset anonymized, no sensitive personal info.
- **Bias & Limitations**: Memory bias, small dataset, subjective notes.
- **Visualization Justification**: Timeline shows journey, salary line quantifies growth, bar chart shows role balance, heatmap shows volunteer intensity.
- **Responsible Decision**: Insights are directional, not predictive.
""")

# 6. Interactivity
st.header("🎛️ Interactivity")
st.write("Use the filters in the sidebar to explore by year and journey type.")
