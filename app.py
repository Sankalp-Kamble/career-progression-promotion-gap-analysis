from pathlib import Path

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
st.subheader("Retention Optimization Dashboard")

st.markdown(
    """
    This dashboard explores career progression patterns, promotion gaps,
    retention opportunities, training needs, and managerial continuity.
    """
)

st.info(
    "This dashboard uses exploratory indicators and scoring thresholds. "
    "These scores are decision-support measures, not validated predictions "
    "of employee attrition or confirmed retention risks."
)


# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "promotion_gap_scoring"
    / "employee_promotion_retention_scores.csv"
)
st.write("Dashboard data path:", DATA_PATH)
st.write("File exists:", DATA_PATH.exists())


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.write(
        "Check that employee_promotion_retention_scores.csv "
        "exists inside outputs/promotion_gap_scoring/."
    )
    st.stop()

df = load_data(DATA_PATH)


# ---------------------------------------------------------
# 3. COLUMN DETECTION
# ---------------------------------------------------------

def find_column(candidates):
    """Return the first matching column name."""
    for column in candidates:
        if column in df.columns:
            return column
    return None


COL_CLUSTER = find_column(["CareerCluster", "Career_Cluster"])

COL_PROMOTION_SCORE = find_column([
    "PromotionGapRiskScore",
    "Promotion_Gap_Risk_Score"
])

COL_PROMOTION_CATEGORY = find_column([
    "RiskCategory",
    "PromotionGapRiskCategory",
    "PromotionGapRiskLevel"
])

COL_RETENTION_INDEX = find_column([
    "RetentionOpportunityIndex",
    "Retention_Opportunity_Index"
])

COL_RETENTION_CATEGORY = find_column([
    "OpportunityCategory",
    "RetentionOpportunityCategory",
    "RetentionOpportunitySignal"
])

COL_DEPARTMENT = find_column(["Department"])
COL_JOB_ROLE = find_column(["JobRole", "Job_Role"])
COL_CAREER_STAGE = find_column(["CareerStage", "Career_Stage"])

COL_TRAINING = find_column([
    "TrainingNeedIndicator",
    "Training_Need_Indicator"
])

COL_MANAGER = find_column([
    "ManagerStabilityImpact",
    "ManagerStabilityCategory"
])

COL_RECORD_ID = find_column(["EmployeeRecordID"])


# Display detected columns for verification
st.write("Detected Promotion Score Column:", COL_PROMOTION_SCORE)
st.write("Detected Risk Category Column:", COL_PROMOTION_CATEGORY)
st.write("Detected Retention Index Column:", COL_RETENTION_INDEX)
st.write("Detected Opportunity Category:", COL_RETENTION_CATEGORY)


# Validate essential columns
required_columns = [
    COL_CLUSTER,
    COL_PROMOTION_SCORE,
    COL_PROMOTION_CATEGORY,
    COL_RETENTION_INDEX,
    COL_RETENTION_CATEGORY,
    COL_DEPARTMENT,
    COL_JOB_ROLE
]

if any(column is None for column in required_columns):

    st.error("Some required columns were not found.")

    st.write("Available CSV columns:", df.columns.tolist())

    st.stop()


# ---------------------------------------------------------
# 4. DATA PREPARATION
# ---------------------------------------------------------

df[COL_PROMOTION_SCORE] = pd.to_numeric(
    df[COL_PROMOTION_SCORE], errors="coerce"
)

df[COL_RETENTION_INDEX] = pd.to_numeric(
    df[COL_RETENTION_INDEX], errors="coerce"
)

for column in [COL_CLUSTER, COL_DEPARTMENT, COL_JOB_ROLE]:
    df[column] = df[column].fillna("Unknown").astype(str)

if COL_RECORD_ID is None:
    df["DashboardRecordID"] = range(1, len(df) + 1)
    COL_RECORD_ID = "DashboardRecordID"


# ---------------------------------------------------------
# 5. SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()


def add_multiselect_filter(data, column, label):
    if column is None:
        return data

    values = sorted(data[column].dropna().astype(str).unique())

    selected = st.sidebar.multiselect(
        label,
        options=values,
        default=values
    )

    if selected:
        data = data[data[column].astype(str).isin(selected)]

    return data


filtered_df = add_multiselect_filter(
    filtered_df, COL_DEPARTMENT, "Department"
)

filtered_df = add_multiselect_filter(
    filtered_df, COL_JOB_ROLE, "Job Role"
)

filtered_df = add_multiselect_filter(
    filtered_df, COL_CLUSTER, "Career Cluster"
)

filtered_df = add_multiselect_filter(
    filtered_df, COL_CAREER_STAGE, "Career Stage"
)

filtered_df = add_multiselect_filter(
    filtered_df, COL_PROMOTION_CATEGORY, "Promotion Gap Risk"
)

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Records after filtering: {len(filtered_df):,}"
)

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# ---------------------------------------------------------
# 6. MAIN KPI SECTION
# ---------------------------------------------------------

st.header("Overall Career and Retention Indicators")

total_records = len(filtered_df)

high_risk_count = (
    filtered_df[COL_PROMOTION_CATEGORY]
    .astype(str)
    .str.contains("High", case=False, na=False)
    .sum()
)

high_opportunity_count = (
    filtered_df[COL_RETENTION_CATEGORY]
    .astype(str)
    .str.contains("High Opportunity", case=False, na=False)
    .sum()
)

medium_opportunity_count = (
    filtered_df[COL_RETENTION_CATEGORY]
    .astype(str)
    .str.contains("Medium Opportunity", case=False, na=False)
    .sum()
)

avg_promotion_score = filtered_df[
    COL_PROMOTION_SCORE
].mean()

avg_retention_index = filtered_df[
    COL_RETENTION_INDEX
].mean()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Employee Records", f"{total_records:,}")
k2.metric("High Promotion Risk", f"{high_risk_count:,}")
k3.metric("High Retention Opportunity", f"{high_opportunity_count:,}")
k4.metric(
    "Average Promotion Risk Score",
    f"{avg_promotion_score:.2f}" if pd.notna(avg_promotion_score) else "N/A"
)
k5.metric(
    "Average Retention Index",
    f"{avg_retention_index:.2f}" if pd.notna(avg_retention_index) else "N/A"
)

st.markdown("---")


# ---------------------------------------------------------
# 7. DASHBOARD TABS
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

    st.header("Career Path Clustering Dashboard")

    st.write(
        "Explore the distribution and promotion-risk patterns "
        "across the identified career clusters."
    )

    col1, col2 = st.columns(2)

    with col1:
        cluster_counts = (
            filtered_df[COL_CLUSTER]
            .value_counts()
            .rename_axis("Career Cluster")
            .reset_index(name="Employee Count")
        )

        fig = px.bar(
            cluster_counts,
            x="Career Cluster",
            y="Employee Count",
            title="Employee Distribution by Career Cluster",
            text="Employee Count"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cluster_risk = (
            filtered_df.groupby(COL_CLUSTER)[COL_PROMOTION_SCORE]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            cluster_risk,
            x=COL_CLUSTER,
            y=COL_PROMOTION_SCORE,
            title="Average Promotion Gap Risk by Cluster",
            labels={
                COL_CLUSTER: "Career Cluster",
                COL_PROMOTION_SCORE: "Average Risk Score"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Career Cluster Summary")

    cluster_summary = (
        filtered_df.groupby(COL_CLUSTER)
        .agg(
            Employee_Count=(COL_RECORD_ID, "count"),
            Average_Promotion_Risk=(COL_PROMOTION_SCORE, "mean"),
            Average_Retention_Index=(COL_RETENTION_INDEX, "mean")
        )
        .reset_index()
    )

    st.dataframe(
        cluster_summary.round(2),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 2: PROMOTION GAP MONITOR
# =========================================================

with tab2:

    st.header("Promotion Gap Monitor")

    st.write(
        "Monitor the distribution of promotion-gap risk "
        "and compare risk across departments and job roles."
    )

    col1, col2 = st.columns(2)

    with col1:
        risk_counts = (
            filtered_df[COL_PROMOTION_CATEGORY]
            .fillna("Unknown")
            .value_counts()
            .rename_axis("Risk Category")
            .reset_index(name="Employee Count")
        )

        fig = px.pie(
            risk_counts,
            names="Risk Category",
            values="Employee Count",
            title="Promotion Gap Risk Distribution",
            hole=0.35
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        department_risk = (
            filtered_df.groupby(COL_DEPARTMENT)[COL_PROMOTION_SCORE]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            department_risk,
            x=COL_DEPARTMENT,
            y=COL_PROMOTION_SCORE,
            title="Average Promotion Risk by Department",
            labels={
                COL_DEPARTMENT: "Department",
                COL_PROMOTION_SCORE: "Average Risk Score"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Promotion Risk by Job Role")

    role_risk = (
        filtered_df.groupby(COL_JOB_ROLE)[COL_PROMOTION_SCORE]
        .mean()
        .reset_index()
        .sort_values(COL_PROMOTION_SCORE, ascending=False)
    )

    fig = px.bar(
        role_risk,
        x=COL_PROMOTION_SCORE,
        y=COL_JOB_ROLE,
        orientation="h",
        title="Average Promotion Risk by Job Role"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        role_risk.round(2),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3: RETENTION OPPORTUNITY PANEL
# =========================================================

with tab3:

    st.header("Retention Opportunity Panel")

    st.write(
        "Explore employees who may benefit from career-development "
        "interventions based on promotion gaps and engagement proxies."
    )

    col1, col2 = st.columns(2)

    with col1:
        opportunity_counts = (
            filtered_df[COL_RETENTION_CATEGORY]
            .fillna("Unknown")
            .value_counts()
            .rename_axis("Opportunity Category")
            .reset_index(name="Employee Count")
        )

        fig = px.pie(
            opportunity_counts,
            names="Opportunity Category",
            values="Employee Count",
            title="Retention Opportunity Distribution",
            hole=0.35
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        opportunity_by_department = (
            filtered_df.groupby(COL_DEPARTMENT)[COL_RETENTION_INDEX]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            opportunity_by_department,
            x=COL_DEPARTMENT,
            y=COL_RETENTION_INDEX,
            title="Average Retention Opportunity Index by Department"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Employees for Potential Career Interventions")

    opportunity_records = filtered_df[
        filtered_df[COL_RETENTION_CATEGORY]
        .astype(str)
        .isin(["High Opportunity", "Medium Opportunity"])
    ].copy()

    display_columns = [
        COL_RECORD_ID,
        COL_DEPARTMENT,
        COL_JOB_ROLE,
        COL_CLUSTER,
        COL_PROMOTION_SCORE,
        COL_PROMOTION_CATEGORY,
        COL_RETENTION_INDEX,
        COL_RETENTION_CATEGORY
    ]

    if COL_CAREER_STAGE:
        display_columns.append(COL_CAREER_STAGE)

    display_columns = list(dict.fromkeys(display_columns))

    st.write(
        f"Records meeting the high or medium opportunity criteria: "
        f"{len(opportunity_records):,}"
    )

    st.dataframe(
        opportunity_records[display_columns].round(2),
        use_container_width=True,
        hide_index=True
    )

    csv_data = opportunity_records[display_columns].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Opportunity Records (CSV)",
        data=csv_data,
        file_name="retention_opportunity_records.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 4: MANAGERIAL INSIGHT DASHBOARD
# =========================================================

with tab4:

    st.header("Managerial Insight Dashboard")

    st.write(
        "Examine managerial continuity and training requirements "
        "to support career-development planning."
    )

    col1, col2 = st.columns(2)

    with col1:

        if COL_MANAGER:

            manager_counts = (
                filtered_df[COL_MANAGER]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Manager Stability")
                .reset_index(name="Employee Count")
            )

            fig = px.bar(
                manager_counts,
                x="Manager Stability",
                y="Employee Count",
                title="Managerial Continuity Distribution",
                text="Employee Count"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning(
                "Manager stability field was not found in the dataset."
            )

    with col2:

        if COL_TRAINING:

            training_counts = (
                filtered_df[COL_TRAINING]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Training Need")
                .reset_index(name="Employee Count")
            )

            fig = px.bar(
                training_counts,
                x="Training Need",
                y="Employee Count",
                title="Training Need Distribution",
                text="Employee Count"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning(
                "Training need field was not found in the dataset."
            )

    st.subheader("Department-Level Managerial and Training Summary")

    summary_data = filtered_df.copy()

    if COL_MANAGER and COL_TRAINING:

        managerial_summary = (
            summary_data.groupby(COL_DEPARTMENT)
            .agg(
                Employee_Count=(COL_RECORD_ID, "count"),
                Average_Promotion_Risk=(COL_PROMOTION_SCORE, "mean"),
                Average_Retention_Index=(COL_RETENTION_INDEX, "mean"),
                Manager_Stability_Categories=(COL_MANAGER, "nunique"),
                Training_Need_Categories=(COL_TRAINING, "nunique")
            )
            .reset_index()
        )

        st.dataframe(
            managerial_summary.round(2),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "The department summary requires both manager stability "
            "and training need fields."
        )


# ---------------------------------------------------------
# 8. FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Career Progression and Promotion Gap Analysis | "
    "Unified Mentor Project"
)

st.caption(
    "Generated record IDs are row-level reference numbers, "
    "not verified employee identifiers. All risk and opportunity "
    "categories should be validated with HR stakeholders."
)
