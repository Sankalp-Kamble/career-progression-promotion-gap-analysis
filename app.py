
import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Career Progression & Retention Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Career Progression and Promotion Gap Analysis")
st.subheader("Aggregated Retention Optimization Dashboard")

st.markdown(
    """
    This dashboard presents aggregated findings from an exploratory
    employee career progression analysis, covering promotion gaps,
    career clusters, retention opportunity indicators, training needs,
    and managerial continuity.
    """
)

st.info(
    "All figures shown are aggregated project results. "
    "Promotion risk and retention opportunity scores are exploratory "
    "decision-support indicators, not validated predictions or "
    "confirmed employee retention risks."
)


# ---------------------------------------------------------
# 2. AGGREGATED PROJECT DATA
# ---------------------------------------------------------

# Overall project statistics
TOTAL_RECORDS = 1470
AVERAGE_PROMOTION_RISK = 46.14
AVERAGE_RETENTION_INDEX = 49.61

# Career cluster distribution
cluster_data = pd.DataFrame({
    "Career Cluster": ["Cluster 0", "Cluster 1", "Cluster 2"],
    "Record Count": [205, 879, 386],
    "Average Promotion Risk": [45.86, 36.71, 66.84],
    "Average Retention Index": [49.42, 43.01, 64.12]
})

# Promotion gap risk distribution
risk_data = pd.DataFrame({
    "Risk Category": ["Low", "Medium", "High", "Not Applicable"],
    "Record Count": [717, 503, 206, 44]
})

# Retention opportunity distribution
opportunity_data = pd.DataFrame({
    "Opportunity Category": [
        "No Immediate Opportunity Signal",
        "Medium Opportunity",
        "High Opportunity",
        "Low Opportunity",
        "Insufficient Data"
    ],
    "Record Count": [1057, 222, 130, 17, 44]
})

# Department-level analysis
department_data = pd.DataFrame({
    "Department": ["Human Resources", "R&D", "Sales"],
    "Record Count": [63, 961, 446],
    "Average Promotion Risk": [42.35, 45.30, 48.51],
    "Average Retention Index": [46.39, 49.06, 51.30],
    "High Risk Records": [6, 128, 72],
    "High Opportunity Records": [5, 80, 45]
})

# Managerial continuity distribution
manager_data = pd.DataFrame({
    "Manager Continuity": [
        "Moderate Continuity",
        "High Continuity",
        "Low Continuity",
        "Not Assessed"
    ],
    "Record Count": [606, 462, 358, 44]
})

# Training need distribution
training_data = pd.DataFrame({
    "Training Need": ["Low", "Moderate", "High"],
    "Record Count": [798, 566, 106]
})


# ---------------------------------------------------------
# 3. SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("Project Information")

st.sidebar.markdown(
    """
    **Project:** Career Progression and Promotion Gap
    Analysis for Retention Optimization

    **Project:** Unified Mentor Internship

    **Analysis:** Exploratory HR Analytics

    **Methods:** K-Means Clustering, Hierarchical
    Clustering and Rule-Based Scoring
    """
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Public dashboard containing aggregated project findings only."
)


# ---------------------------------------------------------
# 4. OVERALL KPI SECTION
# ---------------------------------------------------------

st.header("Overall Project Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Records Analysed", f"{TOTAL_RECORDS:,}")
k2.metric("High Promotion Risk", "206")
k3.metric("High Retention Opportunity", "130")
k4.metric("High + Medium Opportunity", "352")

k5, k6 = st.columns(2)

k5.metric(
    "Average Promotion Gap Risk Score",
    f"{AVERAGE_PROMOTION_RISK:.2f}"
)

k6.metric(
    "Average Retention Opportunity Index",
    f"{AVERAGE_RETENTION_INDEX:.2f}"
)

st.markdown("---")


# ---------------------------------------------------------
# 5. DASHBOARD TABS
# ---------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Career Path Clustering",
    "Promotion Gap Monitor",
    "Retention Opportunity",
    "Managerial Insights"
])


# =========================================================
# TAB 1: CAREER PATH CLUSTERING
# =========================================================

with tab1:

    st.header("Career Path Clustering")

    st.write(
        "K-Means clustering identified three broad career profiles. "
        "Cluster labels are descriptive group identifiers."
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            cluster_data,
            x="Career Cluster",
            y="Record Count",
            text="Record Count",
            title="Record Distribution Across Career Clusters"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            cluster_data,
            x="Career Cluster",
            y="Average Promotion Risk",
            text="Average Promotion Risk",
            title="Average Promotion Risk by Cluster"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Career Cluster Profile")

    st.dataframe(
        cluster_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        **Interpretation:**

        - Cluster 0 represents a group with moderate average career
          experience and relatively higher salary hikes.
        - Cluster 1 is the largest group and has the lowest average
          promotion risk score among the three clusters.
        - Cluster 2 represents a more experienced, longer-tenure
          group and has the highest average promotion risk score.
        """
    )

    st.caption(
        "The selected three-cluster solution achieved a silhouette "
        "score of 0.3305. This indicates moderate separation, not "
        "perfectly distinct career groups."
    )


# =========================================================
# TAB 2: PROMOTION GAP MONITOR
# =========================================================

with tab2:

    st.header("Promotion Gap Risk Monitor")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            risk_data,
            names="Risk Category",
            values="Record Count",
            hole=0.35,
            title="Promotion Gap Risk Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            department_data,
            x="Department",
            y="Average Promotion Risk",
            text="Average Promotion Risk",
            title="Average Promotion Risk by Department"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Promotion Risk Summary")

    st.dataframe(
        risk_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Department-Level Promotion Risk")

    st.dataframe(
        department_data[
            [
                "Department",
                "Record Count",
                "Average Promotion Risk",
                "High Risk Records"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        **Key observation:** Sales has the highest average
        promotion risk score (48.51), followed by R&D (45.30)
        and Human Resources (42.35).

        These are descriptive comparisons and do not establish
        that department membership causes promotion delays.
        """
    )


# =========================================================
# TAB 3: RETENTION OPPORTUNITY
# =========================================================

with tab3:

    st.header("Retention Opportunity Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            opportunity_data,
            names="Opportunity Category",
            values="Record Count",
            hole=0.35,
            title="Retention Opportunity Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            department_data,
            x="Department",
            y="Average Retention Index",
            text="Average Retention Index",
            title="Average Retention Opportunity Index by Department"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Retention Opportunity Summary")

    st.dataframe(
        opportunity_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Department-Level Opportunity Indicators")

    st.dataframe(
        department_data[
            [
                "Department",
                "Record Count",
                "Average Retention Index",
                "High Opportunity Records"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        **Key observation:**

        The scoring framework identified 130 records in the
        High Opportunity category and 222 in the Medium
        Opportunity category.

        These 352 records meet the project's exploratory
        intervention criteria. They should not be interpreted
        as 352 confirmed employee retention risks.
        """
    )


# =========================================================
# TAB 4: MANAGERIAL INSIGHTS
# =========================================================

with tab4:

    st.header("Managerial and Training Insights")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            manager_data,
            x="Manager Continuity",
            y="Record Count",
            text="Record Count",
            title="Managerial Continuity Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            training_data,
            x="Training Need",
            y="Record Count",
            text="Record Count",
            title="Training Need Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Managerial Continuity Summary")

    st.dataframe(
        manager_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Training Need Summary")

    st.dataframe(
        training_data,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        **Potential managerial actions:**

        - Review career development plans for employees experiencing
          extended promotion gaps.
        - Encourage structured career conversations between managers
          and employees.
        - Prioritise relevant learning and development interventions.
        - Review managerial continuity as part of broader career
          progression discussions.
        """
    )


# ---------------------------------------------------------
# 6. METHODOLOGY AND LIMITATIONS
# ---------------------------------------------------------

st.markdown("---")

with st.expander("Methodology and interpretation"):

    st.markdown(
        """
        **Clustering:** K-Means was evaluated across multiple values
        of K. Three clusters produced the highest silhouette score
        among the tested solutions (0.3305).

        **Promotion Gap Risk Score:** Calculated using a weighted
        combination of promotion-gap and role-stagnation indicators.

        **Retention Opportunity Index:** Combines the promotion-gap
        risk score and an engagement proxy derived from job
        satisfaction and job involvement.

        **Limitations:**

        - Risk thresholds are exploratory and require HR validation.
        - Engagement proxy is not a direct measure of intent to stay.
        - The analysis is descriptive and does not establish causality.
        - The dataset's provenance as actual Palo Alto Networks
          employee data has not been independently verified.
        - Results should not be used as individual employment decisions.
        """
    )


# ---------------------------------------------------------
# 7. FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Career Progression and Promotion Gap Analysis | Unified Mentor Project"
)

st.caption(
    "Public portfolio dashboard | Aggregated project results only"
)
