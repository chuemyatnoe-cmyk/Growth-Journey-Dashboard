import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="My Growth Journey Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Chue Myat Noe_Personal Story Dataset.csv")

    # Clean dates
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

    # Clean salary columns
    df['Annual Avg Salary (MMK)'] = pd.to_numeric(
        df['Annual Avg Salary (MMK)']
        .astype(str)
        .str.replace("~", "")
        .str.replace(",", ""),
        errors='coerce'
    )

    df['Cumulative Salary Growth (MMK)'] = pd.to_numeric(
        df['Cumulative Salary Growth (MMK)']
        .astype(str)
        .str.replace(",", ""),
        errors='coerce'
    )

    # Clean duration
    df['Duration (Months)'] = pd.to_numeric(
        df['Duration (Months)'],
        errors='coerce'
    )

    return df


df = load_data()

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go to:",
    [
        "Home",
        "Data Visualizations",
        "Key Insights",
        "Ethics & Responsibility"
    ]
)

# ---------------------------------------------------
# TOP FILTERS
# ---------------------------------------------------
st.markdown("## 🎛️ Dashboard Filters")

f1, f2, f3 = st.columns(3)

# Year Filter
with f1:
    selected_years = st.multiselect(
        "Year",
        options=sorted(df['Year'].unique()),
        default=sorted(df['Year'].unique())
    )

# Journey Type Filter
with f2:
    selected_journey = st.multiselect(
        "Journey Type",
        options=df['Journey Type'].unique(),
        default=df['Journey Type'].unique()
    )

# Organization Filter
with f3:
    selected_org = st.multiselect(
        "Organization",
        options=df['Organization/Event'].unique(),
        default=df['Organization/Event'].unique()
    )

# Apply filters
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Journey Type'].isin(selected_journey)) &
    (df['Organization/Event'].isin(selected_org))
]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.markdown("## 📌 Overview Metrics")

k1, k2, k3, k4 = st.columns(4)

total_roles = len(filtered_df)

volunteer_roles = len(
    filtered_df[
        filtered_df['Journey Type'] == "Volunteer"
    ]
)

highest_salary = filtered_df[
    'Annual Avg Salary (MMK)'
].max()

organizations = filtered_df[
    'Organization/Event'
].nunique()

with k1:
    st.metric(
        "Total Roles",
        total_roles
    )

with k2:
    st.metric(
        "Volunteer Roles",
        volunteer_roles
    )

with k3:
    st.metric(
        "Highest Salary (MMK)",
        f"{int(highest_salary):,}"
    )

with k4:
    st.metric(
        "Organizations Joined",
        organizations
    )

st.markdown("---")

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "Home":

    st.title("📖 My Growth Journey Dashboard")

    st.markdown("""
    ### Volunteering, Employment, and Salary Growth Journey

    This dashboard transforms my personal experiences into structured
    data to analyze how volunteering and employment opportunities
    shaped my professional development and salary growth over time.

    This project explores:
    - How volunteering influenced career opportunities
    - Which roles contributed most to growth
    - How salary increased over time
    - What future decisions can improve career development
    """)

    st.markdown("---")

    st.subheader("📂 Dataset Preview")

    st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------
# DATA VISUALIZATIONS PAGE
# ---------------------------------------------------
elif page == "Data Visualizations":

    st.title("📊 Data Visualizations")

    # ---------------------------------------------------
    # VOLUNTEER TIMELINE
    # ---------------------------------------------------
    st.subheader("📅 Volunteering Journey Across Organizations")

    volunteer_df = filtered_df[
        filtered_df['Journey Type'] == "Volunteer"
    ]

    fig_timeline = px.bar(
        volunteer_df,
        x="Duration (Months)",
        y="Organization/Event",
        orientation="h",
        color="Year",
        text="Duration (Months)",
        hover_data=["Role"],
        title="Volunteer Journey Timeline"
    )

    fig_timeline.update_layout(
        xaxis_title="Duration (Months)",
        yaxis_title="Organization",
        legend_title="Year"
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    st.caption("""
    Insight:
    Long-term volunteering improved leadership,
    communication, and teamwork skills.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # EMPLOYMENT ROLES BAR CHART
    # ---------------------------------------------------
    st.subheader("💼 Employment Roles and Work Duration")

    employment_df = filtered_df[
        filtered_df['Journey Type'] == "Employment"
    ]

    fig_employment = px.bar(
        employment_df,
        x="Duration (Months)",
        y="Role",
        orientation="h",
        color="Year",
        text="Duration (Months)",
        hover_data=["Organization/Event"],
        title="Work Experience Duration by Role"
    )

    fig_employment.update_layout(
        xaxis_title="Duration Worked (Months)",
        yaxis_title="Employment Role",
        legend_title="Year"
    )

    st.plotly_chart(fig_employment, use_container_width=True)

    st.caption("""
    Insight:
    Longer employment duration reflects increasing
    professional stability and responsibility.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # SALARY GROWTH LINE CHART
    # ---------------------------------------------------
    st.subheader("📈 Salary Growth Journey")

    salary_df = filtered_df.dropna(
        subset=['Cumulative Salary Growth (MMK)']
    )

    fig_salary = px.line(
        salary_df,
        x="Year",
        y="Cumulative Salary Growth (MMK)",
        color="Journey Type",
        markers=True,
        hover_data=[
            "Organization/Event",
            "Role"
        ],
        title="Salary Growth Across My Journey"
    )

    fig_salary.update_layout(
        xaxis_title="Year",
        yaxis_title="Cumulative Salary Growth (MMK)",
        legend_title="Journey Type"
    )

    st.plotly_chart(fig_salary, use_container_width=True)

    st.caption("""
    Insight:
    Salary growth accelerated after gaining more
    leadership and employment experience.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # VOLUNTEER VS EMPLOYMENT
    # ---------------------------------------------------
    st.subheader("📊 Volunteer vs Employment Roles")

    fig_roles = px.histogram(
        filtered_df,
        x="Journey Type",
        color="Journey Type"
    )

    st.plotly_chart(fig_roles, use_container_width=True)

    st.caption("""
    Insight:
    Volunteering experiences created the foundation
    for later employment opportunities.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # ORGANIZATION PARTICIPATION
    # ---------------------------------------------------
    st.subheader("🏢 Organization Participation")

    org_counts = filtered_df[
        'Organization/Event'
    ].value_counts().reset_index()

    org_counts.columns = [
        'Organization/Event',
        'Count'
    ]

    fig_org = px.bar(
        org_counts,
        x='Organization/Event',
        y='Count',
        color='Count',
        title='Participation Across Organizations'
    )

    fig_org.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_org, use_container_width=True)

    st.caption("""
    Insight:
    Participating in multiple organizations improved
    adaptability, networking, and leadership skills.
    """)

# ---------------------------------------------------
# KEY INSIGHTS PAGE
# ---------------------------------------------------
elif page == "Key Insights":

    st.title("🔍 Key Insights")

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Strongest Skill",
        "Leadership"
    )

    c2.metric(
        "Career Turning Point",
        "2024"
    )

    c3.metric(
        "Main Growth Driver",
        "Volunteering"
    )

    c4.metric(
        "Biggest Achievement",
        "Salary Growth"
    )

    st.markdown("---")

    st.success("""
    Volunteering created opportunities to build leadership,
    teamwork, and communication skills.
    """)

    st.info("""
    Employment roles contributed significantly
    to salary growth and professional development.
    """)

    st.warning("""
    Managing volunteering, academics,
    and employment simultaneously was challenging.
    """)

    st.error("""
    Some periods involved high workloads
    and stress from balancing multiple responsibilities.
    """)

    st.markdown("---")

    st.subheader("🎯 Future Decisions")

    st.markdown("""
    Based on the data, I should:

    1. Continue joining meaningful leadership opportunities
    2. Focus on long-term professional growth
    3. Improve technical and communication skills
    4. Maintain balance between work and volunteering
    5. Prioritize sustainable career opportunities
    """)

# ---------------------------------------------------
# ETHICS PAGE
# ---------------------------------------------------
elif page == "Ethics & Responsibility":

    st.title("⚖️ Ethics & Responsibility")

    st.markdown("---")

    st.header("🔒 Privacy Statement")

    st.info("""
    - Sensitive personal information was removed
    - Third-party identities were anonymized
    - Salary values were simplified for academic purposes
    - Dataset used only for educational storytelling
    """)

    st.markdown("---")

    st.header("⚠️ Bias & Limitations")

    with st.expander("Memory Bias"):
        st.write("""
        Some experiences rely on personal memory,
        which may affect accuracy.
        """)

    with st.expander("Small Dataset"):
        st.write("""
        The dataset is limited and may not fully represent
        long-term professional development.
        """)

    with st.expander("Subjective Interpretation"):
        st.write("""
        Leadership impact and personal growth
        are difficult to measure numerically.
        """)

    st.markdown("---")

    st.header("📊 Visualization Justification")

    st.success("""
    - Timeline chart visualizes volunteering progression
    - Employment chart shows work experience duration
    - Salary line chart highlights growth trends
    - Participation chart shows organizational involvement
    """)

    st.markdown("---")

    st.header("🎯 Responsible Interpretation")

    st.warning("""
    This dashboard identifies trends and reflections,
    not direct causation.

    Career growth is influenced by multiple factors,
    including education, economic conditions,
    and personal opportunities.
    """)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <center style='color: gray; font-size: 0.85em;'>
    DATA 201 – Final Dashboard Project |
    Chue Myat Noe
    </center>
    """,
    unsafe_allow_html=True
)
