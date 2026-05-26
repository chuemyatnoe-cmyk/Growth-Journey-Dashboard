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

st.sidebar.markdown("---")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🎛️ Dashboard Filters")

# Year Filter
selected_years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

# Journey Type Filter
selected_journey = st.sidebar.multiselect(
    "Select Journey Type",
    options=df['Journey Type'].unique(),
    default=df['Journey Type'].unique()
)

# Apply filters
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Journey Type'].isin(selected_journey))
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

employment_roles = len(
    filtered_df[
        filtered_df['Journey Type'] == "Employment"
    ]
)

highest_salary = filtered_df[
    'Annual Avg Salary (MMK)'
].max()

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
        "Employment Roles",
        employment_roles
    )

with k4:
    st.metric(
        "Highest Salary (MMK)",
        f"{int(highest_salary):,}"
    )

st.markdown("---")

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "Home":

    st.title("📖 My Growth Journey Dashboard")

    st.markdown("""

### Volunteering, Leadership, and Salary Growth Journey

    This dashboard transforms my personal experiences into data-driven insights.
    It explores how volunteering, leadership roles, and organizational involvement
    shaped my professional growth and salary development over time.

    Through this project, I wanted to understand:
    
    - How volunteering contributed to my career opportunities
    - Which years showed the biggest growth
    - How leadership experiences influenced my development
    - What decisions I should make differently in the future
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
    # VOLUNTEER JOURNEY CHART
    # ---------------------------------------------------
    st.subheader("📅 Volunteer Journey Timeline")

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
        title="Volunteer Experience Duration"
    )

    fig_timeline.update_layout(
        xaxis_title="Duration (Months)",
        yaxis_title="Organization",
        legend_title="Year"
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    st.caption("""
    Insight:
    Long-term volunteering strengthened leadership,
    teamwork, and communication skills.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # EMPLOYMENT ROLE CHART
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
        title="Employment Experience Duration"
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
    # SALARY GROWTH CHART
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
    communication, and teamwork skills.
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
    Some periods involved stress from balancing
    multiple responsibilities at once.
    """)

    st.markdown("---")

    st.subheader("🎯 Future Decisions")

    st.markdown("""
    Based on the data, I should:

    1. Continue joining meaningful leadership opportunities
    2. Improve technical and professional skills
    3. Maintain balance between volunteering and work
    4. Focus on sustainable career growth
    5. Continue building professional networks
    """)

# ---------------------------------------------------
# ETHICS PAGE
# ---------------------------------------------------
elif page == "Ethics & Responsibility":

    st.title("⚖️ Ethics & Responsibility")

    st.markdown("---")

    # Privacy
    st.header("🔒 Privacy Statement")

    st.info("""
    - Sensitive personal information was removed
    - Third-party identities were anonymized
    - Salary values were simplified for educational purposes
    - Dataset used only for academic storytelling
    """)

    st.markdown("---")

    # Bias & Limitations
    st.header("⚠️ Bias & Limitations")

    with st.expander("Memory Bias"):
        st.write("""
        Some experiences rely on personal reflection
        and memory, which may affect accuracy.
        """)

    with st.expander("Small Dataset"):
        st.write("""
        The dataset is limited and may not fully represent
        long-term career development.
        """)

    with st.expander("Subjective Interpretation"):
        st.write("""
        Leadership impact and personal growth
        are difficult to measure numerically.
        """)

    st.markdown("---")

    # Visualization Justification
    st.header("📊 Visualization Justification")

    st.success("""
    - Volunteer bar chart visualizes volunteer journey duration
    - Employment chart shows work experience duration
    - Salary line chart highlights career growth over time
    - Histogram compares volunteer and employment experiences
    """)

    st.markdown("---")

    # Responsible Decision
    st.header("🎯 Responsible Interpretation")

    st.warning("""
    This dashboard identifies patterns and reflections,
    not direct causation.

    Career growth depends on multiple factors including
    education, economic conditions, opportunities,
    and personal development.
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
