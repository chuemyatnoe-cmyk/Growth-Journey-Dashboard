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

    # Clean date columns
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
# SIDEBAR NAVIGATION ONLY
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
# TOP FILTERS INSIDE DASHBOARD
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

# Metrics calculations
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

# KPI Cards
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
    ### Volunteering, Leadership, and Salary Growth Journey

    This dashboard transforms my personal experiences into structured data
    to explore how volunteering and leadership opportunities shaped my
    career growth and salary development over time.

    Through this project, I wanted to understand:

    - How volunteering contributed to professional opportunities
    - Which years showed the greatest growth
    - How leadership roles influenced my career
    - What future decisions I should make differently
    """)

    st.markdown("---")

    st.subheader("📂 Dataset Preview")

    st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------
# DATA VISUALIZATION PAGE
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
    Long-term volunteering experiences strengthened leadership,
    teamwork, and communication skills.
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
    leadership and organizational experience.
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
    Volunteering experiences formed the foundation
    of professional development.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # ORGANIZATION PARTICIPATION
    # ---------------------------------------------------
    st.subheader("🏢 Participation Across Organizations")

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
        title='Organization Participation'
    )

    fig_org.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_org, use_container_width=True)

    st.caption("""
    Insight:
    Joining different organizations improved adaptability,
    networking, and leadership development.
    """)

# ---------------------------------------------------
# KEY INSIGHTS PAGE
# ---------------------------------------------------
elif page == "Key Insights":

    st.title("🔍 Key Insights")

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Strongest Growth Area",
        "Leadership"
    )

    c2.metric(
        "Career Turning Point",
        "2024"
    )

    c3.metric(
        "Main Contribution",
        "Volunteering"
    )

    c4.metric(
        "Biggest Achievement",
        "Salary Growth"
    )

    st.markdown("---")

    st.success("""
    Volunteering created opportunities for leadership,
    networking, and communication development.
    """)

    st.info("""
    Salary growth became more visible after taking
    leadership and organizational responsibilities.
    """)

    st.warning("""
    Balancing volunteering, academics,
    and employment remained challenging.
    """)

    st.error("""
    Some periods created stress due to handling
    multiple responsibilities simultaneously.
    """)

    st.markdown("---")

    st.subheader("🎯 Future Decisions")

    st.markdown("""
    Based on the data, I should:

    1. Continue joining meaningful leadership opportunities
    2. Focus on long-term projects with stronger impact
    3. Build more technical and professional skills
    4. Improve balance between volunteering and work
    5. Prioritize sustainable career growth opportunities
    """)

# ---------------------------------------------------
# ETHICS PAGE
# ---------------------------------------------------
elif page == "Ethics & Responsibility":

    st.title("⚖️ Ethics & Responsibility")

    st.markdown("---")

    # PRIVACY
    st.header("🔒 Privacy Statement")

    st.info("""
    - All sensitive personal information was removed.
    - Third-party identities were anonymized.
    - Salary values were simplified for educational use.
    - The dataset is used only for academic storytelling.
    """)

    st.markdown("---")

    # BIAS
    st.header("⚠️ Bias & Limitations")

    with st.expander("Memory Bias"):
        st.write("""
        Some experiences rely on personal reflection,
        which may affect accuracy.
        """)

    with st.expander("Small Dataset"):
        st.write("""
        The dataset is limited and cannot fully represent
        long-term professional development.
        """)

    with st.expander("Subjective Interpretation"):
        st.write("""
        Leadership impact and personal growth
        are difficult to measure numerically.
        """)

    st.markdown("---")

    # VISUALIZATION JUSTIFICATION
    st.header("📊 Visualization Justification")

    st.success("""
    - Timeline chart visualizes volunteering progression
    - Salary line chart shows growth trends over time
    - Histogram compares volunteer and employment experiences
    - Organization chart highlights participation and networking
    """)

    st.markdown("---")

    # RESPONSIBLE DECISION
    st.header("🎯 Responsible Interpretation")

    st.warning("""
    This dashboard identifies patterns and reflections,
    not direct causation.

    Volunteering may contribute to growth,
    but educational, economic,
    and social factors also influence outcomes.
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
