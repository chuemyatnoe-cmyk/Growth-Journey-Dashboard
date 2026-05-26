import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="My Growth Journey Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
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

st.sidebar.markdown("---")

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------
st.sidebar.header("🎛️ Filters")

# Filter by Journey Type
journey_filter = st.sidebar.multiselect(
    "Select Journey Type",
    options=df['Journey Type'].unique(),
    default=df['Journey Type'].unique()
)

# Filter by Year
year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

# Apply filters
filtered_df = df[
    (df['Journey Type'].isin(journey_filter)) &
    (df['Year'].isin(year_filter))
]

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
    - Now I can see what I achieve throughout these years but I got a lot of rejections to grow. 
    - To get a job, I got at least 5 rejections from the companies and their main reason is that I don't have a degree because the roles that I applied are customer service and operations. 
    - As all you see, now I study Data Science but my working experiences are totally different from my study.
    """)

    st.markdown("---")

    # KPI SECTION
    st.header("📌 General Overview")

    col1, col2, col3, col4 = st.columns(4)

    # Total roles
    total_roles = len(filtered_df)

    # Volunteer roles
    volunteer_roles = len(
        filtered_df[
            filtered_df['Journey Type'] == "Volunteer"
        ]
    )

    # Highest salary
    highest_salary = filtered_df[
        'Annual Avg Salary (MMK)'
    ].max()

    # Organizations
    total_orgs = filtered_df[
        'Organization/Event'
    ].nunique()

    with col1:
        st.metric(
            "Total Roles",
            total_roles
        )

    with col2:
        st.metric(
            "Volunteer Roles",
            volunteer_roles
        )

    with col3:
        st.metric(
            "Highest Salary (MMK)",
            f"{int(highest_salary):,}"
        )

    with col4:
        st.metric(
            "Organizations Joined",
            total_orgs
        )

    st.markdown("---")

    st.subheader("📂 Dataset Preview")

    st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------
# DATA VISUALIZATION PAGE
# ---------------------------------------------------
elif page == "Data Visualizations":

    st.title("📊 Data Visualizations")

    # ---------------------------------------------------
    # VOLUNTEERING TIMELINE
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
    Insight: Long-term volunteering experiences helped build leadership,
    communication, and organizational skills.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # SALARY GROWTH
    # ---------------------------------------------------
    st.subheader("📈 Salary Growth Over Time")

    salary_growth = filtered_df.dropna(
        subset=['Cumulative Salary Growth (MMK)']
    )

    fig_salary = px.line(
        salary_growth,
        x="Year",
        y="Cumulative Salary Growth (MMK)",
        markers=True,
        title="Cumulative Salary Growth"
    )

    st.plotly_chart(fig_salary, use_container_width=True)

    st.caption("""
    Insight: Salary growth accelerated after gaining more leadership
    and organizational experiences.
    """)

    st.markdown("---")

    # ---------------------------------------------------
    # JOURNEY TYPE DISTRIBUTION
    # ---------------------------------------------------
    st.subheader("📊 Volunteer vs Employment Roles")

    fig_roles = px.histogram(
        filtered_df,
        x="Journey Type",
        color="Journey Type"
    )

    st.plotly_chart(fig_roles, use_container_width=True)

    st.caption("""
    Insight: Volunteering experiences formed a major foundation
    for professional development.
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
    Insight: Joining different organizations improved adaptability,
    networking, and teamwork skills.
    """)

# ---------------------------------------------------
# KEY INSIGHTS PAGE
# ---------------------------------------------------
elif page == "Key Insights":

    st.title("🔍 Key Insights")

    st.markdown("---")

    # KPI INSIGHTS
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

    st.subheader("📌 Main Findings")

    st.success("""
    Volunteering experiences created opportunities for leadership development,
    networking, and communication skills.
    """)

    st.info("""
    Salary growth became more visible after taking leadership and
    organizational responsibilities.
    """)

    st.warning("""
    Balancing volunteering, academics, and career development
    remained a challenge throughout the journey.
    """)

    st.error("""
    Some experiences created stress and workload pressure,
    especially during periods with multiple responsibilities.
    """)

    st.markdown("---")

    st.subheader("🎯 Future Decisions")

    st.markdown("""
    Based on the data, I should:

    1. Continue participating in meaningful leadership opportunities
    2. Focus on long-term projects with higher impact
    3. Build stronger technical and professional skills
    4. Improve work-life balance
    5. Prioritize opportunities that support both growth and sustainability
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
    - No sensitive personal information is included.
    - Third-party identities were anonymized.
    - Salary values are simplified for educational purposes.
    - The dataset is used only for academic storytelling.
    """)

    st.markdown("---")

    # BIAS
    st.header("⚠️ Bias & Limitations")

    with st.expander("Memory Bias"):
        st.write("""
        Some experiences depend on personal memory and reflection,
        which may affect accuracy.
        """)

    with st.expander("Small Dataset"):
        st.write("""
        The dataset is limited and cannot fully represent
        long-term career patterns.
        """)

    with st.expander("Subjective Interpretation"):
        st.write("""
        Leadership impact and growth are partially subjective
        and difficult to measure numerically.
        """)

    st.markdown("---")

    # VISUALIZATION JUSTIFICATION
    st.header("📊 Visualization Justification")

    st.success("""
    - Timeline bar chart shows organizational journey progression
    - Salary line chart shows career growth trends
    - Histogram compares volunteer and employment experiences
    - Organization chart highlights networking and participation
    """)

    st.markdown("---")

    # RESPONSIBLE DECISION
    st.header("🎯 Responsible Interpretation")

    st.warning("""
    This dashboard identifies patterns and reflections,
    not direct causation.

    Volunteering may support career growth,
    but external economic, educational,
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
