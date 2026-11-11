
# ============================================================
# PROJECT: Career Progression and Promotion Gap Analysis
# PHASE 1: Dataset Inspection and Understanding
# ============================================================

import pandas as pd
import json
from pathlib import Path


# ------------------------------------------------------------
# 1. PROJECT PATH
# ------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_DIR / "data" / "Palo Alto Networks.csv"

OUTPUT_DIR = PROJECT_DIR / "outputs" / "dataset_profile"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. EXPECTED DATASET COLUMNS
# ------------------------------------------------------------

EXPECTED_COLUMNS = [
    "Age",
    "Attrition",
    "BusinessTravel",
    "DailyRate",
    "Department",
    "DistanceFromHome",
    "Education",
    "EducationField",
    "EnvironmentSatisfaction",
    "Gender",
    "HourlyRate",
    "JobInvolvement",
    "JobLevel",
    "JobRole",
    "JobSatisfaction",
    "MaritalStatus",
    "MonthlyIncome",
    "MonthlyRate",
    "NumCompaniesWorked",
    "OverTime",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager"
]


# ------------------------------------------------------------
# 3. LOAD DATASET
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("CAREER PROGRESSION ANALYSIS - PHASE 1")
print("DATASET INSPECTION AND UNDERSTANDING")
print("=" * 65)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_PATH}\n"
        "Please check the CSV filename and data folder."
    )

try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(DATA_PATH, encoding="latin1")

print("\nDataset loaded successfully!")


# ------------------------------------------------------------
# 4. DATASET OVERVIEW
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("4. DATASET OVERVIEW")
print("-" * 65)

rows, columns = df.shape

print(f"Total Records       : {rows}")
print(f"Total Columns       : {columns}")
print(f"Memory Usage        : {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

print("\nFirst Five Records:")
print(df.head())

print("\nLast Five Records:")
print(df.tail())

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe(include="all").transpose())


# ------------------------------------------------------------
# 5. COLUMN INVENTORY
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("5. COLUMN INVENTORY")
print("-" * 65)

column_inventory = pd.DataFrame({
    "Column_Name": df.columns,
    "Data_Type": df.dtypes.astype(str).values,
    "Non_Null_Count": df.notnull().sum().values,
    "Missing_Count": df.isnull().sum().values,
    "Unique_Count": df.nunique(dropna=False).values
})

column_inventory["Missing_Percentage"] = (
    column_inventory["Missing_Count"] / len(df) * 100
).round(2)

print(column_inventory.to_string(index=False))

column_inventory.to_csv(
    OUTPUT_DIR / "column_inventory.csv",
    index=False
)


# ------------------------------------------------------------
# 6. VERIFY ALL EXPECTED COLUMNS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("6. EXPECTED COLUMN VALIDATION")
print("-" * 65)

missing_columns = [
    col for col in EXPECTED_COLUMNS
    if col not in df.columns
]

unexpected_columns = [
    col for col in df.columns
    if col not in EXPECTED_COLUMNS
]

print("Expected Columns:", len(EXPECTED_COLUMNS))
print("Actual Columns  :", len(df.columns))
print("Missing Columns :", missing_columns)
print("Unexpected Columns:", unexpected_columns)

if not missing_columns and not unexpected_columns:
    print("SUCCESS: All 31 expected columns are present.")
else:
    print("WARNING: Dataset columns differ from the project specification.")


# ------------------------------------------------------------
# 7. DATA TYPE ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("7. DATA TYPE ANALYSIS")
print("-" * 65)

numeric_columns = df.select_dtypes(include="number").columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nNumerical Columns:")
print(numeric_columns)

print("\nCategorical Columns:")
print(categorical_columns)

print("\nNumerical Column Count:", len(numeric_columns))
print("Categorical Column Count:", len(categorical_columns))


# ------------------------------------------------------------
# 8. MISSING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("8. MISSING VALUE ANALYSIS")
print("-" * 65)

missing_report = pd.DataFrame({
    "Column": df.columns,
    "Missing_Values": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().mean().values * 100
    ).round(2)
})

missing_report = missing_report.sort_values(
    by="Missing_Values",
    ascending=False
)

print(missing_report.to_string(index=False))

print("\nTotal Missing Values:", df.isnull().sum().sum())

missing_report.to_csv(
    OUTPUT_DIR / "missing_value_report.csv",
    index=False
)


# ------------------------------------------------------------
# 9. DUPLICATE ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("9. DUPLICATE ANALYSIS")
print("-" * 65)

duplicate_count = df.duplicated().sum()

print("Total Duplicate Rows:", duplicate_count)

if duplicate_count == 0:
    print("No completely duplicated rows detected.")
else:
    print("Duplicate rows require further investigation.")

# We are NOT deleting duplicates at this stage.


# ------------------------------------------------------------
# 10. UNIQUE VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("10. UNIQUE VALUE ANALYSIS")
print("-" * 65)

unique_report = []

for column in df.columns:

    unique_values = df[column].dropna().unique()

    unique_report.append({
        "Column": column,
        "Unique_Count": df[column].nunique(dropna=False),
        "Sample_Unique_Values": json.dumps(
            [str(value) for value in unique_values[:20]]
        )
    })

unique_report = pd.DataFrame(unique_report)

print(unique_report.to_string(index=False))

unique_report.to_csv(
    OUTPUT_DIR / "unique_value_report.csv",
    index=False
)


# ------------------------------------------------------------
# 11. CATEGORICAL VALUE FREQUENCY
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("11. CATEGORICAL VALUE FREQUENCY")
print("-" * 65)

frequency_reports = []

for column in categorical_columns:

    print(f"\nColumn: {column}")

    print(df[column].value_counts(dropna=False))

    counts = df[column].value_counts(dropna=False)

    for value, count in counts.items():

        frequency_reports.append({
            "Column": column,
            "Value": str(value),
            "Count": count,
            "Percentage": round(count / len(df) * 100, 2)
        })

frequency_report = pd.DataFrame(frequency_reports)

frequency_report.to_csv(
    OUTPUT_DIR / "categorical_frequency_report.csv",
    index=False
)


# ------------------------------------------------------------
# 12. ATTRITION DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("12. ATTRITION DISTRIBUTION")
print("-" * 65)

if "Attrition" in df.columns:

    attrition_counts = df["Attrition"].value_counts(dropna=False)

    attrition_percentages = (
        df["Attrition"].value_counts(normalize=True, dropna=False) * 100
    ).round(2)

    print("\nAttrition Counts:")
    print(attrition_counts)

    print("\nAttrition Percentages:")
    print(attrition_percentages)

    attrition_report = pd.DataFrame({
        "Attrition_Value": attrition_counts.index,
        "Employee_Count": attrition_counts.values,
        "Percentage": attrition_percentages.reindex(
            attrition_counts.index
        ).values
    })

    attrition_report.to_csv(
        OUTPUT_DIR / "attrition_distribution.csv",
        index=False
    )

    invalid_attrition = ~df["Attrition"].isin([0, 1])

    print(
        "\nInvalid Attrition Values:",
        invalid_attrition.sum()
    )


# ------------------------------------------------------------
# 13. CAREER DATA QUALITY CHECKS
# ------------------------------------------------------------

print("\n" + "-" * 65)
print("13. CAREER DATA QUALITY CHECKS")
print("-" * 65)

career_checks = {}

career_checks["Zero_YearsAtCompany"] = (
    df["YearsAtCompany"] == 0
).sum()

career_checks["Role_Years_Exceed_Company_Years"] = (
    df["YearsInCurrentRole"] > df["YearsAtCompany"]
).sum()

career_checks["Promotion_Years_Exceed_Company_Years"] = (
    df["YearsSinceLastPromotion"] > df["YearsAtCompany"]
).sum()

career_checks["Manager_Years_Exceed_Company_Years"] = (
    df["YearsWithCurrManager"] > df["YearsAtCompany"]
).sum()

career_checks["Company_Years_Exceed_Total_Working_Years"] = (
    df["YearsAtCompany"] > df["TotalWorkingYears"]
).sum()

career_checks["Negative_Career_Values"] = (
    df[
        [
            "TotalWorkingYears",
            "YearsAtCompany",
            "YearsInCurrentRole",
            "YearsSinceLastPromotion",
            "YearsWithCurrManager",
            "TrainingTimesLastYear"
        ]
    ] < 0
).any(axis=1).sum()

for check, count in career_checks.items():

    print(f"{check}: {count}")


career_quality_report = pd.DataFrame(
    list(career_checks.items()),
    columns=["Quality_Check", "Affected_Records"]
)

career_quality_report.to_csv(
    OUTPUT_DIR / "career_data_quality_report.csv",
    index=False
)


# ------------------------------------------------------------
# 14. SAVE DESCRIPTIVE STATISTICS
# ------------------------------------------------------------

df.describe(include="all").transpose().to_csv(
    OUTPUT_DIR / "descriptive_statistics.csv"
)


# ------------------------------------------------------------
# 15. FINAL DATASET PROFILE
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PHASE 1 SUMMARY")
print("=" * 65)

print(f"Total Records              : {len(df)}")
print(f"Total Columns              : {len(df.columns)}")
print(f"Missing Values             : {df.isnull().sum().sum()}")
print(f"Duplicate Rows             : {duplicate_count}")
print(f"Numerical Columns           : {len(numeric_columns)}")
print(f"Categorical Columns         : {len(categorical_columns)}")
print(f"Expected Columns Missing    : {len(missing_columns)}")
print(f"Unexpected Columns          : {len(unexpected_columns)}")

print("\nAll reports saved to:")
print(OUTPUT_DIR)

print("\nPHASE 1 DATASET INSPECTION COMPLETED")
print("=" * 65)


# ============================================================
# PROJECT: Career Progression and Promotion Gap Analysis
# PHASE 2: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re

# ------------------------------------------------------------
# 1. PROJECT PATHS AND CONFIGURATION
# ------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_DIR / "data" / "Palo Alto Networks.csv"

OUTPUT_DIR = PROJECT_DIR / "outputs" / "eda"

UNIVARIATE_DIR = OUTPUT_DIR / "univariate"
CAREER_DIR = OUTPUT_DIR / "career_analysis"
ATTRITION_DIR = OUTPUT_DIR / "attrition_analysis"
REPORT_DIR = OUTPUT_DIR / "reports"

for folder in [
    UNIVARIATE_DIR,
    CAREER_DIR,
    ATTRITION_DIR,
    REPORT_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PHASE 2 - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# ------------------------------------------------------------
# 3. DEFINE ANALYTICAL COLUMN GROUPS
# ------------------------------------------------------------

# Categorical variables
CATEGORICAL_COLUMNS = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime"
]

# Ordinal variables: numeric values with an ordered meaning
ORDINAL_COLUMNS = [
    "Education",
    "EnvironmentSatisfaction",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "WorkLifeBalance"
]

# Binary outcome
TARGET_COLUMN = "Attrition"

# Career progression variables
CAREER_COLUMNS = [
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager"
]

# Training and performance variables
DEVELOPMENT_COLUMNS = [
    "TrainingTimesLastYear",
    "PerformanceRating",
    "PercentSalaryHike"
]

# Satisfaction variables
SATISFACTION_COLUMNS = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "RelationshipSatisfaction",
    "WorkLifeBalance",
    "JobInvolvement"
]

# Columns required by this analysis
REQUIRED_COLUMNS = (
    CATEGORICAL_COLUMNS
    + ORDINAL_COLUMNS
    + CAREER_COLUMNS
    + DEVELOPMENT_COLUMNS
    + SATISFACTION_COLUMNS
    + [TARGET_COLUMN]
)

missing_columns = [
    column for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing from dataset: {missing_columns}"
    )

# Identify numeric variables dynamically.
# Attrition and ordinal variables are analyzed as categories,
# not as continuous measurements.

CONTINUOUS_COLUMNS = [
    column
    for column in df.select_dtypes(include="number").columns
    if column not in ORDINAL_COLUMNS + [TARGET_COLUMN]
]

print("\nAnalytical Column Groups:")
print("Categorical:", CATEGORICAL_COLUMNS)
print("Ordinal:", ORDINAL_COLUMNS)
print("Continuous:", CONTINUOUS_COLUMNS)


# ------------------------------------------------------------
# 4. HELPER FUNCTION FOR SAVING CHARTS
# ------------------------------------------------------------

def clean_filename(name):
    """Convert a column name into a safe filename."""

    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def save_chart(filename, folder):
    """Save the current Matplotlib chart."""

    plt.tight_layout()
    plt.savefig(
        folder / filename,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


# ------------------------------------------------------------
# 5. SECTION A: WORKFORCE DEMOGRAPHICS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION A: WORKFORCE DEMOGRAPHICS")
print("-" * 70)

DEMOGRAPHIC_COLUMNS = [
    "Age",
    "Gender",
    "Education",
    "EducationField",
    "MaritalStatus",
    "DistanceFromHome"
]

for column in DEMOGRAPHIC_COLUMNS:

    plt.figure(figsize=(9, 5))

    if column in CATEGORICAL_COLUMNS or column in ORDINAL_COLUMNS:

        counts = df[column].value_counts().sort_index()

        plt.bar(
            counts.index.astype(str),
            counts.values
        )

        plt.xlabel(column)
        plt.ylabel("Number of Employees")

    else:

        plt.hist(
            df[column].dropna(),
            bins=20,
            edgecolor="black"
        )

        plt.xlabel(column)
        plt.ylabel("Frequency")

    plt.title(f"Distribution of {column}")

    save_chart(
        f"{clean_filename(column)}_distribution.png",
        UNIVARIATE_DIR
    )

print("Workforce demographic charts generated.")


# ------------------------------------------------------------
# 6. SECTION B: DEPARTMENT AND JOB ROLE ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION B: DEPARTMENT AND JOB ROLE ANALYSIS")
print("-" * 70)

ORGANIZATION_COLUMNS = [
    "Department",
    "JobRole",
    "JobLevel",
    "BusinessTravel"
]

for column in ORGANIZATION_COLUMNS:

    counts = df[column].value_counts().sort_values(
        ascending=False
    )

    plt.figure(figsize=(11, 6))

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title(f"Employee Distribution by {column}")
    plt.xlabel(column)
    plt.ylabel("Employee Count")
    plt.xticks(rotation=35, ha="right")

    save_chart(
        f"{clean_filename(column)}_distribution.png",
        UNIVARIATE_DIR
    )


# Department-wise employee counts

department_counts = (
    df.groupby("Department")
    .size()
    .reset_index(name="Employee_Count")
)

department_counts.to_csv(
    REPORT_DIR / "department_distribution.csv",
    index=False
)


# Job role-wise employee counts

jobrole_counts = (
    df.groupby("JobRole")
    .size()
    .reset_index(name="Employee_Count")
    .sort_values("Employee_Count", ascending=False)
)

jobrole_counts.to_csv(
    REPORT_DIR / "jobrole_distribution.csv",
    index=False
)

print("Department and job role analysis completed.")


# ------------------------------------------------------------
# 7. SECTION C: CAREER PROGRESSION ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION C: CAREER PROGRESSION ANALYSIS")
print("-" * 70)

# Descriptive statistics of career variables

career_summary = df[CAREER_COLUMNS].describe().transpose()

career_summary.to_csv(
    CAREER_DIR / "career_descriptive_statistics.csv"
)

print("\nCareer Descriptive Statistics:")
print(career_summary)


# Distribution of career progression variables

for column in CAREER_COLUMNS:

    plt.figure(figsize=(9, 5))

    plt.hist(
        df[column].dropna(),
        bins=20,
        edgecolor="black"
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel("Years")
    plt.ylabel("Employee Frequency")

    save_chart(
        f"{clean_filename(column)}_distribution.png",
        CAREER_DIR
    )


# Career variables by department

department_career = (
    df.groupby("Department")[CAREER_COLUMNS]
    .mean()
    .round(2)
)

department_career.to_csv(
    CAREER_DIR / "career_metrics_by_department.csv"
)

print("\nCareer Metrics by Department:")
print(department_career)


# Career variables by job role

jobrole_career = (
    df.groupby("JobRole")[CAREER_COLUMNS]
    .mean()
    .round(2)
)

jobrole_career.to_csv(
    CAREER_DIR / "career_metrics_by_jobrole.csv"
)


# Career variables by job level

joblevel_career = (
    df.groupby("JobLevel")[CAREER_COLUMNS]
    .mean()
    .round(2)
)

joblevel_career.to_csv(
    CAREER_DIR / "career_metrics_by_joblevel.csv"
)


# ------------------------------------------------------------
# 8. SECTION D: TRAINING AND PERFORMANCE ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION D: TRAINING AND PERFORMANCE ANALYSIS")
print("-" * 70)

development_summary = (
    df.groupby("TrainingTimesLastYear")
    .agg(
        Employee_Count=("TrainingTimesLastYear", "size"),
        Average_Performance=("PerformanceRating", "mean"),
        Average_Salary_Hike=("PercentSalaryHike", "mean"),
        Average_Company_Tenure=("YearsAtCompany", "mean")
    )
    .round(2)
)

development_summary.to_csv(
    REPORT_DIR / "training_development_summary.csv"
)

print("\nTraining and Development Summary:")
print(development_summary)


for column in DEVELOPMENT_COLUMNS:

    counts = df[column].value_counts().sort_index()

    plt.figure(figsize=(9, 5))

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Employee Count")

    save_chart(
        f"{clean_filename(column)}_distribution.png",
        UNIVARIATE_DIR
    )


# ------------------------------------------------------------
# 9. SECTION E: MANAGERIAL CONTINUITY ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION E: MANAGERIAL CONTINUITY ANALYSIS")
print("-" * 70)

manager_summary = (
    df.groupby("Department")
    .agg(
        Average_Manager_Tenure=("YearsWithCurrManager", "mean"),
        Average_Role_Tenure=("YearsInCurrentRole", "mean"),
        Average_Promotion_Gap=("YearsSinceLastPromotion", "mean"),
        Employee_Count=("YearsWithCurrManager", "size")
    )
    .round(2)
)

manager_summary.to_csv(
    CAREER_DIR / "managerial_continuity_summary.csv"
)

print("\nManagerial Continuity by Department:")
print(manager_summary)


# Manager tenure versus promotion gap

plt.figure(figsize=(9, 6))

plt.scatter(
    df["YearsWithCurrManager"],
    df["YearsSinceLastPromotion"],
    alpha=0.5
)

plt.title("Manager Tenure vs Years Since Last Promotion")
plt.xlabel("Years With Current Manager")
plt.ylabel("Years Since Last Promotion")

save_chart(
    "manager_tenure_vs_promotion_gap.png",
    CAREER_DIR
)


# ------------------------------------------------------------
# 10. SECTION F: EMPLOYEE SATISFACTION ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION F: EMPLOYEE SATISFACTION ANALYSIS")
print("-" * 70)

satisfaction_summary = df[
    SATISFACTION_COLUMNS
].describe().transpose()

satisfaction_summary.to_csv(
    REPORT_DIR / "satisfaction_summary.csv"
)

for column in SATISFACTION_COLUMNS:

    counts = df[column].value_counts().sort_index()

    plt.figure(figsize=(8, 5))

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel("Rating")
    plt.ylabel("Employee Count")

    save_chart(
        f"{clean_filename(column)}_distribution.png",
        UNIVARIATE_DIR
    )


# ------------------------------------------------------------
# 11. SECTION G: ALL COLUMN DISTRIBUTIONS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION G: ALL COLUMN DISTRIBUTIONS")
print("-" * 70)

# This section ensures every dataset column receives
# an individual distribution chart.

for column in df.columns:

    if column in CATEGORICAL_COLUMNS or column in ORDINAL_COLUMNS:
        counts = df[column].value_counts(dropna=False)

        plt.figure(figsize=(10, 5))

        plt.bar(
            counts.index.astype(str),
            counts.values
        )

        plt.xlabel(column)
        plt.ylabel("Employee Count")

        plt.xticks(rotation=30, ha="right")

    elif column == TARGET_COLUMN:

        counts = df[column].value_counts(dropna=False)

        plt.figure(figsize=(8, 5))

        plt.bar(
            counts.index.astype(str),
            counts.values
        )

        plt.xlabel("Attrition")
        plt.ylabel("Employee Count")

    else:

        plt.figure(figsize=(9, 5))

        plt.hist(
            df[column].dropna(),
            bins=20,
            edgecolor="black"
        )

        plt.xlabel(column)
        plt.ylabel("Frequency")

    plt.title(f"EDA Distribution: {column}")

    save_chart(
        f"all_columns_{clean_filename(column)}.png",
        UNIVARIATE_DIR
    )

print("Distribution charts generated for all dataset columns.")


# ------------------------------------------------------------
# 12. SECTION H: ATTRITION ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION H: ATTRITION ANALYSIS")
print("-" * 70)

# Attrition count and percentage

attrition_summary = (
    df.groupby("Attrition")
    .size()
    .reset_index(name="Employee_Count")
)

attrition_summary["Percentage"] = (
    attrition_summary["Employee_Count"]
    / len(df) * 100
).round(2)

attrition_summary.to_csv(
    ATTRITION_DIR / "attrition_summary.csv",
    index=False
)

print("\nAttrition Summary:")
print(attrition_summary)


# Compare career and continuous variables by attrition

attrition_numeric_summary = (
    df.groupby("Attrition")[CONTINUOUS_COLUMNS]
    .mean()
    .transpose()
    .round(2)
)

attrition_numeric_summary.to_csv(
    ATTRITION_DIR / "numeric_metrics_by_attrition.csv"
)

print("\nNumerical Metrics by Attrition:")
print(attrition_numeric_summary)


# Visualize continuous variables by attrition

for column in CONTINUOUS_COLUMNS:

    grouped_data = [
        df.loc[df["Attrition"] == group, column].dropna()
        for group in sorted(df["Attrition"].dropna().unique())
    ]

    plt.figure(figsize=(8, 5))

    plt.boxplot(
        grouped_data,
        tick_labels=[
            str(group)
            for group in sorted(df["Attrition"].dropna().unique())
        ]
    )

    plt.title(f"{column} by Attrition")
    plt.xlabel("Attrition (0 = No, 1 = Yes)")
    plt.ylabel(column)

    save_chart(
        f"{clean_filename(column)}_by_attrition.png",
        ATTRITION_DIR
    )


# Attrition rates by categorical and ordinal variables

ATTRITION_GROUP_COLUMNS = (
    CATEGORICAL_COLUMNS + ORDINAL_COLUMNS
)

attrition_group_reports = []

for column in ATTRITION_GROUP_COLUMNS:

    group_summary = (
        df.groupby(column, dropna=False)["Attrition"]
        .agg(["count", "mean"])
        .reset_index()
    )

    group_summary.columns = [
        column,
        "Employee_Count",
        "Attrition_Rate"
    ]

    group_summary["Attrition_Rate_Percentage"] = (
        group_summary["Attrition_Rate"] * 100
    ).round(2)

    group_summary["Variable"] = column

    attrition_group_reports.append(group_summary)

    plt.figure(figsize=(10, 5))

    plt.bar(
        group_summary[column].astype(str),
        group_summary["Attrition_Rate_Percentage"]
    )

    plt.title(f"Attrition Rate by {column}")
    plt.xlabel(column)
    plt.ylabel("Attrition Rate (%)")
    plt.xticks(rotation=30, ha="right")

    save_chart(
        f"attrition_by_{clean_filename(column)}.png",
        ATTRITION_DIR
    )


all_attrition_groups = pd.concat(
    attrition_group_reports,
    ignore_index=True
)

all_attrition_groups.to_csv(
    ATTRITION_DIR / "attrition_by_category.csv",
    index=False
)


# ------------------------------------------------------------
# 13. DEPARTMENT AND JOB ROLE ATTRITION ANALYSIS
# ------------------------------------------------------------

department_attrition = (
    df.groupby("Department")["Attrition"]
    .agg(["count", "mean"])
    .reset_index()
)

department_attrition.columns = [
    "Department",
    "Employee_Count",
    "Attrition_Rate"
]

department_attrition["Attrition_Rate_Percentage"] = (
    department_attrition["Attrition_Rate"] * 100
).round(2)

department_attrition.to_csv(
    ATTRITION_DIR / "department_attrition.csv",
    index=False
)


jobrole_attrition = (
    df.groupby("JobRole")["Attrition"]
    .agg(["count", "mean"])
    .reset_index()
)

jobrole_attrition.columns = [
    "JobRole",
    "Employee_Count",
    "Attrition_Rate"
]

jobrole_attrition["Attrition_Rate_Percentage"] = (
    jobrole_attrition["Attrition_Rate"] * 100
).round(2)

jobrole_attrition.to_csv(
    ATTRITION_DIR / "jobrole_attrition.csv",
    index=False
)


# ------------------------------------------------------------
# 14. CORRELATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SECTION I: CORRELATION ANALYSIS")
print("-" * 70)

correlation_data = df.select_dtypes(
    include="number"
)

correlation_matrix = correlation_data.corr()

correlation_matrix.to_csv(
    REPORT_DIR / "correlation_matrix.csv"
)

print("\nCorrelation Matrix:")
print(correlation_matrix.round(2))


# Correlation heatmap using Matplotlib

plt.figure(figsize=(16, 12))

image = plt.imshow(
    correlation_matrix,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    aspect="auto"
)

plt.colorbar(image, label="Correlation")

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns,
    rotation=90
)

plt.yticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns
)

plt.title("Numerical Variable Correlation Heatmap")

save_chart(
    "correlation_heatmap.png",
    REPORT_DIR
)


# ------------------------------------------------------------
# 15. CAREER VARIABLE RELATIONSHIPS
# ------------------------------------------------------------

career_correlation = df[CAREER_COLUMNS].corr()

career_correlation.to_csv(
    CAREER_DIR / "career_correlation_matrix.csv"
)


plt.figure(figsize=(10, 7))

image = plt.imshow(
    career_correlation,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.colorbar(image, label="Correlation")

plt.xticks(
    range(len(CAREER_COLUMNS)),
    CAREER_COLUMNS,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(CAREER_COLUMNS)),
    CAREER_COLUMNS
)

plt.title("Career Variables Correlation Heatmap")

save_chart(
    "career_correlation_heatmap.png",
    CAREER_DIR
)


# ------------------------------------------------------------
# 16. ALL COLUMN COVERAGE VALIDATION
# ------------------------------------------------------------

coverage_report = pd.DataFrame({
    "Column": df.columns,
    "EDA_Distribution_Generated": True,
    "Missing_Values": df.isnull().sum().values,
    "Unique_Values": df.nunique(dropna=False).values
})

coverage_report.to_csv(
    REPORT_DIR / "eda_column_coverage.csv",
    index=False
)

print("\nAll dataset columns included in EDA:")
print(coverage_report.to_string(index=False))


# ------------------------------------------------------------
# 17. FINAL PHASE SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PHASE 2 - EDA COMPLETED")
print("=" * 70)

print("Total Employees:", len(df))
print("Total Dataset Columns:", len(df.columns))
print("Distribution Charts Generated:", len(df.columns))
print("Career Variables Analyzed:", len(CAREER_COLUMNS))
print("Development Variables Analyzed:", len(DEVELOPMENT_COLUMNS))
print("Satisfaction Variables Analyzed:", len(SATISFACTION_COLUMNS))
print("Attrition Comparisons Completed:", len(CONTINUOUS_COLUMNS))

print("\nEDA Reports Saved At:")
print(OUTPUT_DIR)

print("\nPHASE 2 EXECUTION SUCCESSFUL")
print("=" * 70)


from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Palo Alto Networks.csv"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "preprocessing"

REPORT_DIR = OUTPUT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("\n" + "=" * 65)
print("PHASE 3: DATA CLEANING AND PREPROCESSING")
print("=" * 65)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

print("\nOriginal dataset loaded successfully.")
print("Dataset shape:", df.shape)


# Preserve the original data for comparison
original_df = df.copy()


# ============================================================
# 3. DATASET STRUCTURE AND COLUMN DEFINITIONS
# ============================================================

TARGET_COLUMN = "Attrition"

CATEGORICAL_COLUMNS = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime"
]

ORDINAL_COLUMNS = [
    "Education",
    "EnvironmentSatisfaction",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "WorkLifeBalance"
]

CAREER_COLUMNS = [
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager"
]

DEVELOPMENT_COLUMNS = [
    "TrainingTimesLastYear",
    "PerformanceRating",
    "PercentSalaryHike"
]

SATISFACTION_COLUMNS = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "RelationshipSatisfaction",
    "WorkLifeBalance",
    "JobInvolvement"
]


# Validate essential columns
required_columns = (
    CATEGORICAL_COLUMNS
    + ORDINAL_COLUMNS
    + CAREER_COLUMNS
    + DEVELOPMENT_COLUMNS
    + SATISFACTION_COLUMNS
    + [TARGET_COLUMN]
)

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )


# ============================================================
# 4. INITIAL DATA QUALITY REPORT
# ============================================================

quality_report = pd.DataFrame({
    "Metric": [
        "Original Rows",
        "Original Columns",
        "Missing Values",
        "Duplicate Rows",
        "Total Missing Cells"
    ],
    "Value": [
        len(df),
        len(df.columns),
        int(df.isnull().any(axis=1).sum()),
        int(df.duplicated().sum()),
        int(df.isnull().sum().sum())
    ]
})

quality_report.to_csv(
    REPORT_DIR / "initial_data_quality.csv",
    index=False
)


# ============================================================
# 5. HANDLE MISSING VALUES
# ============================================================

missing_before = df.isnull().sum()

missing_report = pd.DataFrame({
    "Column": missing_before.index,
    "Missing_Before": missing_before.values
})

# Impute numerical columns using median
numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

for column in numeric_columns:

    if df[column].isnull().any():

        median_value = df[column].median()

        df[column] = df[column].fillna(median_value)


# Impute categorical columns using mode
categorical_data_columns = df.select_dtypes(
    exclude=np.number
).columns.tolist()

for column in categorical_data_columns:

    if df[column].isnull().any():

        mode_values = df[column].mode(dropna=True)

        if not mode_values.empty:
            df[column] = df[column].fillna(
                mode_values.iloc[0]
            )
        else:
            df[column] = df[column].fillna("Unknown")


missing_report["Missing_After"] = [
    int(df[column].isnull().sum())
    for column in missing_report["Column"]
]

missing_report.to_csv(
    REPORT_DIR / "missing_value_treatment.csv",
    index=False
)


# ============================================================
# 6. REMOVE EXACT DUPLICATE ROWS
# ============================================================

duplicates_before = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

duplicates_after = int(df.duplicated().sum())

print("\nDuplicate rows removed:", duplicates_before)


# ============================================================
# 7. CAREER DATA VALIDATION
# ============================================================

career_validation = pd.DataFrame(index=df.index)

career_validation["Zero_YearsAtCompany"] = (
    df["YearsAtCompany"] == 0
)

career_validation["CurrentRole_Exceeds_CompanyTenure"] = (
    df["YearsInCurrentRole"] > df["YearsAtCompany"]
)

career_validation["PromotionYears_Exceed_CompanyTenure"] = (
    df["YearsSinceLastPromotion"] > df["YearsAtCompany"]
)

career_validation["ManagerTenure_Exceeds_CompanyTenure"] = (
    df["YearsWithCurrManager"] > df["YearsAtCompany"]
)

career_validation["CompanyTenure_Exceeds_TotalExperience"] = (
    df["YearsAtCompany"] > df["TotalWorkingYears"]
)

career_validation["Negative_Career_Values"] = (
    df[CAREER_COLUMNS].lt(0).any(axis=1)
)

career_validation_report = pd.DataFrame({
    "Validation_Check": career_validation.columns,
    "Flagged_Records": career_validation.sum().values
})

career_validation_report.to_csv(
    REPORT_DIR / "career_validation_report.csv",
    index=False
)

# Record all rows with at least one career inconsistency
inconsistent_mask = career_validation.any(axis=1)

career_review = df.loc[inconsistent_mask].copy()

career_review.to_csv(
    REPORT_DIR / "career_records_for_review.csv",
    index=False
)

print(
    "Career records flagged for review:",
    int(inconsistent_mask.sum())
)

# Do not automatically delete career-inconsistent records.
# Keep them in the cleaned dataset for transparent analysis.


# ============================================================
# 8. NUMERICAL OUTLIER DETECTION USING IQR
# ============================================================

# Detect outliers in continuous numerical columns.
# Ordinal and binary variables are excluded.

excluded_from_outlier_detection = (
    ORDINAL_COLUMNS + [TARGET_COLUMN]
)

continuous_columns = [
    col for col in df.select_dtypes(include=np.number).columns
    if col not in excluded_from_outlier_detection
]

outlier_records = []

for column in continuous_columns:

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    outlier_mask = (
        (df[column] < lower_limit)
        | (df[column] > upper_limit)
    )

    outlier_records.append({
        "Column": column,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Lower_Limit": lower_limit,
        "Upper_Limit": upper_limit,
        "Outlier_Count": int(outlier_mask.sum()),
        "Outlier_Percentage": round(
            outlier_mask.mean() * 100, 2
        )
    })

outlier_report = pd.DataFrame(outlier_records)

outlier_report.to_csv(
    REPORT_DIR / "numerical_outlier_report.csv",
    index=False
)

print("\nOutlier detection completed.")


# ============================================================
# 9. SAVE CLEANED DATASET
# ============================================================

CLEANED_PATH = OUTPUT_DIR / "cleaned_employee_data.csv"

df.to_csv(CLEANED_PATH, index=False)

print("\nCleaned dataset saved successfully.")


# ============================================================
# 10. ONE-HOT ENCODING OF CATEGORICAL VARIABLES
# ============================================================

encoding_columns = [
    col for col in CATEGORICAL_COLUMNS
    if col in df.columns
]

encoded_df = pd.get_dummies(
    df,
    columns=encoding_columns,
    drop_first=False,
    dtype=int
)

encoded_df.to_csv(
    OUTPUT_DIR / "encoded_employee_data.csv",
    index=False
)

print("Categorical encoding completed.")


# ============================================================
# 11. SCALE NUMERICAL CAREER FEATURES
# ============================================================

# Scale career variables and selected development variables.
# Ordinal fields and Attrition are deliberately excluded.

scaling_columns = [
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "TrainingTimesLastYear",
    "PercentSalaryHike"
]

scaling_columns = [
    col for col in scaling_columns
    if col in df.columns
]

scaled_df = encoded_df.copy()

scaler = StandardScaler()

scaled_df[scaling_columns] = scaler.fit_transform(
    df[scaling_columns]
)

scaled_df.to_csv(
    OUTPUT_DIR / "scaled_employee_data.csv",
    index=False
)

print("Numerical feature scaling completed.")


# ============================================================
# 12. SAVE SCALER PARAMETERS
# ============================================================

scaler_report = pd.DataFrame({
    "Feature": scaling_columns,
    "Mean": scaler.mean_,
    "Standard_Deviation": scaler.scale_
})

scaler_report.to_csv(
    REPORT_DIR / "scaling_parameters.csv",
    index=False
)


# ============================================================
# 13. FINAL PREPROCESSING REPORT
# ============================================================

final_report = pd.DataFrame({
    "Metric": [
        "Original Records",
        "Final Records",
        "Original Columns",
        "Final Encoded Columns",
        "Duplicate Rows Removed",
        "Missing Cells Remaining",
        "Career Records Flagged",
        "Categorical Columns Encoded",
        "Numerical Columns Scaled"
    ],
    "Value": [
        len(original_df),
        len(df),
        len(original_df.columns),
        len(encoded_df.columns),
        duplicates_before,
        int(df.isnull().sum().sum()),
        int(inconsistent_mask.sum()),
        len(encoding_columns),
        len(scaling_columns)
    ]
})

final_report.to_csv(
    REPORT_DIR / "final_preprocessing_summary.csv",
    index=False
)


# ============================================================
# 14. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 65)
print("PREPROCESSING COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nOriginal dataset shape:", original_df.shape)
print("Cleaned dataset shape:", df.shape)
print("Encoded dataset shape:", encoded_df.shape)
print("Scaled dataset shape:", scaled_df.shape)

print(
    "\nMissing values remaining:",
    int(df.isnull().sum().sum())
)

print(
    "Duplicate rows remaining:",
    int(df.duplicated().sum())
)

print("\nOutput files saved in:")
print(OUTPUT_DIR)

print("\nGenerated reports:")
for file in sorted(REPORT_DIR.glob("*.csv")):
    print("-", file.name)

print("\nPhase 3 finished. Please review the output files.")


from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "preprocessing"
    / "cleaned_employee_data.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "feature_engineering"
)

REPORT_DIR = OUTPUT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD CLEANED DATASET
# ============================================================

print("\n" + "=" * 65)
print("PHASE 4: FEATURE ENGINEERING")
print("=" * 65)

if not INPUT_PATH.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {INPUT_PATH}\n"
        "Please complete Phase 3 first."
    )

df = pd.read_csv(INPUT_PATH)

print("\nCleaned dataset loaded successfully.")
print("Original shape:", df.shape)


# ============================================================
# 3. REQUIRED COLUMNS
# ============================================================

required_columns = [
    "YearsAtCompany",
    "YearsSinceLastPromotion",
    "YearsInCurrentRole",
    "TrainingTimesLastYear",
    "YearsWithCurrManager",
    "TotalWorkingYears",
    "JobLevel",
    "JobRole",
    "Department",
    "PerformanceRating",
    "PercentSalaryHike",
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "WorkLifeBalance"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )


# ============================================================
# 4. SAFE DIVISION FUNCTION
# ============================================================

def safe_ratio(numerator, denominator):
    """
    Calculate a ratio safely.

    If denominator is zero, return NaN.
    This avoids creating misleading infinite values.
    """

    return np.divide(
        numerator,
        denominator,
        out=np.full(len(numerator), np.nan, dtype=float),
        where=denominator.to_numpy() != 0
    )


# ============================================================
# 5. PROMOTION GAP RATIO
# ============================================================

df["PromotionGapRatio"] = safe_ratio(
    df["YearsSinceLastPromotion"],
    df["YearsAtCompany"]
)

# Percentage representation
df["PromotionGapPercentage"] = (
    df["PromotionGapRatio"] * 100
)

# Employees with zero company tenure are marked as
# Not Applicable rather than assigned an artificial ratio.


# ============================================================
# 6. ROLE STAGNATION INDEX
# ============================================================

df["RoleStagnationIndex"] = safe_ratio(
    df["YearsInCurrentRole"],
    df["YearsAtCompany"]
)

df["RoleStagnationPercentage"] = (
    df["RoleStagnationIndex"] * 100
)


# ============================================================
# 7. TRAINING INTENSITY SCORE
# ============================================================

df["TrainingIntensityScore"] = safe_ratio(
    df["TrainingTimesLastYear"],
    df["YearsAtCompany"]
)


# ============================================================
# 8. MANAGER STABILITY INDICATOR
# ============================================================

df["ManagerStabilityIndicator"] = safe_ratio(
    df["YearsWithCurrManager"],
    df["YearsAtCompany"]
)

df["ManagerStabilityPercentage"] = (
    df["ManagerStabilityIndicator"] * 100
)


# ============================================================
# 9. CAREER GROWTH INDICATOR
# ============================================================

df["YearsSinceLastPromotion_Absolute"] = (
    df["YearsSinceLastPromotion"]
)

df["CareerGrowthOpportunityYears"] = (
    df["YearsAtCompany"]
    - df["YearsSinceLastPromotion"]
)


# ============================================================
# 10. CAREER STAGE CLASSIFICATION
# ============================================================

def classify_career_stage(years):
    if years <= 2:
        return "Early Career"

    elif years <= 5:
        return "Developing Career"

    elif years <= 10:
        return "Mid Career"

    else:
        return "Experienced Career"


df["CareerStage"] = df["TotalWorkingYears"].apply(
    classify_career_stage
)


# ============================================================
# 11. PROMOTION GAP CATEGORY
# ============================================================

def classify_promotion_gap(row):

    tenure = row["YearsAtCompany"]
    gap = row["YearsSinceLastPromotion"]

    if tenure == 0:
        return "Not Applicable"

    if gap >= 5:
        return "High Promotion Gap"

    elif gap >= 3:
        return "Moderate Promotion Gap"

    else:
        return "Low Promotion Gap"


df["PromotionGapCategory"] = df.apply(
    classify_promotion_gap,
    axis=1
)


# ============================================================
# 12. ROLE STAGNATION CATEGORY
# ============================================================

def classify_role_stagnation(row):

    tenure = row["YearsAtCompany"]
    role_years = row["YearsInCurrentRole"]

    if tenure == 0:
        return "Not Applicable"

    ratio = role_years / tenure

    if ratio >= 0.80 and role_years >= 5:
        return "High Role Stagnation"

    elif ratio >= 0.60 and role_years >= 3:
        return "Moderate Role Stagnation"

    else:
        return "Low Role Stagnation"


df["RoleStagnationCategory"] = df.apply(
    classify_role_stagnation,
    axis=1
)


# ============================================================
# 13. TRAINING NEED INDICATOR
# ============================================================

def classify_training_need(row):

    training = row["TrainingTimesLastYear"]
    performance = row["PerformanceRating"]

    if training <= 1 and performance <= 3:
        return "High Training Need"

    elif training <= 2:
        return "Moderate Training Need"

    else:
        return "Low Training Need"


df["TrainingNeedIndicator"] = df.apply(
    classify_training_need,
    axis=1
)


# ============================================================
# 14. MANAGER STABILITY CATEGORY
# ============================================================

def classify_manager_stability(row):

    tenure = row["YearsAtCompany"]

    if tenure == 0:
        return "Not Applicable"

    ratio = (
        row["YearsWithCurrManager"] / tenure
    )

    if ratio >= 0.80:
        return "High Manager Continuity"

    elif ratio >= 0.40:
        return "Moderate Manager Continuity"

    else:
        return "Low Manager Continuity"


df["ManagerStabilityCategory"] = df.apply(
    classify_manager_stability,
    axis=1
)


# ============================================================
# 15. RETENTION OPPORTUNITY SIGNAL
# ============================================================

# This is an exploratory signal, not a prediction of attrition.
# It deliberately does not use the Attrition column.

df["RetentionOpportunitySignal"] = (
    (df["PromotionGapRatio"] >= 0.50)
    & (df["RoleStagnationIndex"] >= 0.60)
    & (df["YearsAtCompany"] >= 3)
)

df["RetentionOpportunitySignal"] = (
    df["RetentionOpportunitySignal"]
    .map({
        True: "Potential Opportunity",
        False: "No Strong Signal"
    })
)


# ============================================================
# 16. DATA VALIDATION FOR ENGINEERED FEATURES
# ============================================================

engineered_columns = [
    "PromotionGapRatio",
    "PromotionGapPercentage",
    "RoleStagnationIndex",
    "RoleStagnationPercentage",
    "TrainingIntensityScore",
    "ManagerStabilityIndicator",
    "ManagerStabilityPercentage",
    "CareerGrowthOpportunityYears"
]

feature_quality_report = pd.DataFrame({
    "Feature": engineered_columns,
    "Missing_Values": [
        df[column].isnull().sum()
        for column in engineered_columns
    ],
    "Minimum": [
        df[column].min()
        for column in engineered_columns
    ],
    "Maximum": [
        df[column].max()
        for column in engineered_columns
    ],
    "Mean": [
        df[column].mean()
        for column in engineered_columns
    ]
})

feature_quality_report.to_csv(
    REPORT_DIR / "engineered_feature_quality.csv",
    index=False
)


# ============================================================
# 17. SAVE FEATURE-ENGINEERED DATASET
# ============================================================

OUTPUT_PATH = (
    OUTPUT_DIR / "employee_data_with_features.csv"
)

df.to_csv(OUTPUT_PATH, index=False)

print("\nFeature-engineered dataset saved successfully.")


# ============================================================
# 18. SAVE CAREER STAGE DISTRIBUTION
# ============================================================

career_stage_report = (
    df["CareerStage"]
    .value_counts()
    .rename_axis("CareerStage")
    .reset_index(name="EmployeeCount")
)

career_stage_report.to_csv(
    REPORT_DIR / "career_stage_distribution.csv",
    index=False
)


# ============================================================
# 19. SAVE PROMOTION GAP DISTRIBUTION
# ============================================================

promotion_report = (
    df["PromotionGapCategory"]
    .value_counts()
    .rename_axis("PromotionGapCategory")
    .reset_index(name="EmployeeCount")
)

promotion_report.to_csv(
    REPORT_DIR / "promotion_gap_distribution.csv",
    index=False
)


# ============================================================
# 20. SAVE ROLE STAGNATION DISTRIBUTION
# ============================================================

stagnation_report = (
    df["RoleStagnationCategory"]
    .value_counts()
    .rename_axis("RoleStagnationCategory")
    .reset_index(name="EmployeeCount")
)

stagnation_report.to_csv(
    REPORT_DIR / "role_stagnation_distribution.csv",
    index=False
)


# ============================================================
# 21. SAVE TRAINING NEED DISTRIBUTION
# ============================================================

training_report = (
    df["TrainingNeedIndicator"]
    .value_counts()
    .rename_axis("TrainingNeedIndicator")
    .reset_index(name="EmployeeCount")
)

training_report.to_csv(
    REPORT_DIR / "training_need_distribution.csv",
    index=False
)


# ============================================================
# 22. SAVE MANAGER STABILITY DISTRIBUTION
# ============================================================

manager_report = (
    df["ManagerStabilityCategory"]
    .value_counts()
    .rename_axis("ManagerStabilityCategory")
    .reset_index(name="EmployeeCount")
)

manager_report.to_csv(
    REPORT_DIR / "manager_stability_distribution.csv",
    index=False
)


# ============================================================
# 23. SAVE RETENTION OPPORTUNITY SUMMARY
# ============================================================

retention_report = (
    df["RetentionOpportunitySignal"]
    .value_counts()
    .rename_axis("RetentionOpportunitySignal")
    .reset_index(name="EmployeeCount")
)

retention_report.to_csv(
    REPORT_DIR / "retention_opportunity_distribution.csv",
    index=False
)


# ============================================================
# 24. DEPARTMENT-WISE CAREER ANALYSIS
# ============================================================

department_report = (
    df.groupby("Department", dropna=False)
    .agg(
        EmployeeCount=("Department", "size"),
        AveragePromotionGap=("PromotionGapRatio", "mean"),
        AverageRoleStagnation=("RoleStagnationIndex", "mean"),
        AverageTrainingIntensity=("TrainingIntensityScore", "mean"),
        AverageManagerStability=("ManagerStabilityIndicator", "mean")
    )
    .reset_index()
)

department_report.to_csv(
    REPORT_DIR / "department_career_indicators.csv",
    index=False
)


# ============================================================
# 25. JOB ROLE-WISE CAREER ANALYSIS
# ============================================================

role_report = (
    df.groupby("JobRole", dropna=False)
    .agg(
        EmployeeCount=("JobRole", "size"),
        AveragePromotionGap=("PromotionGapRatio", "mean"),
        AverageRoleStagnation=("RoleStagnationIndex", "mean"),
        AverageTrainingIntensity=("TrainingIntensityScore", "mean"),
        AverageManagerStability=("ManagerStabilityIndicator", "mean")
    )
    .reset_index()
)

role_report.to_csv(
    REPORT_DIR / "jobrole_career_indicators.csv",
    index=False
)


# ============================================================
# 26. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("PHASE 4 COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nOriginal number of columns:", df.shape[1])
print("Final dataset shape:", df.shape)

print("\nNew features created:")

for column in engineered_columns:
    print("-", column)

print("\nNew categorical indicators:")

for column in [
    "CareerStage",
    "PromotionGapCategory",
    "RoleStagnationCategory",
    "TrainingNeedIndicator",
    "ManagerStabilityCategory",
    "RetentionOpportunitySignal"
]:
    print("-", column)

print("\nOutput saved to:")
print(OUTPUT_DIR)

print("\nReports saved to:")
print(REPORT_DIR)

print("\nPlease review the generated reports before Phase 5.")


from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "feature_engineering"
    / "employee_data_with_features.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "career_progression_analysis"
)

REPORT_DIR = OUTPUT_DIR / "reports"
CHART_DIR = OUTPUT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("PHASE 5: CAREER PROGRESSION ANALYSIS")
print("=" * 70)

if not INPUT_PATH.exists():
    raise FileNotFoundError(
        f"Feature-engineered dataset not found: {INPUT_PATH}\n"
        "Please complete Phase 4 first."
    )

df = pd.read_csv(INPUT_PATH)

print("\nDataset loaded successfully.")
print("Dataset shape:", df.shape)


# ============================================================
# 3. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Department",
    "JobRole",
    "JobLevel",
    "Attrition",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "PerformanceRating",
    "PercentSalaryHike",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "TrainingIntensityScore",
    "ManagerStabilityIndicator",
    "CareerStage",
    "PromotionGapCategory",
    "RoleStagnationCategory",
    "TrainingNeedIndicator",
    "ManagerStabilityCategory",
    "RetentionOpportunitySignal"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# 4. BASIC CAREER PROGRESSION STATISTICS
# ============================================================

career_variables = [
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "TrainingIntensityScore",
    "ManagerStabilityIndicator"
]

career_summary = df[career_variables].describe().T

career_summary.to_csv(
    REPORT_DIR / "overall_career_summary.csv"
)

print("\nOverall career summary generated.")


# ============================================================
# 5. PROMOTION GAP ANALYSIS
# ============================================================

promotion_summary = (
    df.groupby("PromotionGapCategory", dropna=False)
    .agg(
        EmployeeCount=("PromotionGapCategory", "size"),
        AverageYearsSincePromotion=(
            "YearsSinceLastPromotion", "mean"
        ),
        AverageCompanyTenure=(
            "YearsAtCompany", "mean"
        ),
        AveragePromotionGapRatio=(
            "PromotionGapRatio", "mean"
        )
    )
    .reset_index()
)

promotion_summary.to_csv(
    REPORT_DIR / "promotion_gap_analysis.csv",
    index=False
)


# Department-wise promotion gap
department_promotion = (
    df.groupby("Department", dropna=False)
    .agg(
        EmployeeCount=("Department", "size"),
        AverageYearsSincePromotion=(
            "YearsSinceLastPromotion", "mean"
        ),
        AveragePromotionGapRatio=(
            "PromotionGapRatio", "mean"
        ),
        HighPromotionGapEmployees=(
            "PromotionGapCategory",
            lambda x: (x == "High Promotion Gap").sum()
        )
    )
    .reset_index()
)

department_promotion.to_csv(
    REPORT_DIR / "department_promotion_analysis.csv",
    index=False
)


# Job-role-wise promotion gap
role_promotion = (
    df.groupby("JobRole", dropna=False)
    .agg(
        EmployeeCount=("JobRole", "size"),
        AverageYearsSincePromotion=(
            "YearsSinceLastPromotion", "mean"
        ),
        AveragePromotionGapRatio=(
            "PromotionGapRatio", "mean"
        ),
        HighPromotionGapEmployees=(
            "PromotionGapCategory",
            lambda x: (x == "High Promotion Gap").sum()
        )
    )
    .reset_index()
)

role_promotion.to_csv(
    REPORT_DIR / "jobrole_promotion_analysis.csv",
    index=False
)


# ============================================================
# 6. ROLE STAGNATION ANALYSIS
# ============================================================

stagnation_summary = (
    df.groupby("RoleStagnationCategory", dropna=False)
    .agg(
        EmployeeCount=("RoleStagnationCategory", "size"),
        AverageYearsInCurrentRole=(
            "YearsInCurrentRole", "mean"
        ),
        AverageCompanyTenure=(
            "YearsAtCompany", "mean"
        ),
        AverageRoleStagnationIndex=(
            "RoleStagnationIndex", "mean"
        )
    )
    .reset_index()
)

stagnation_summary.to_csv(
    REPORT_DIR / "role_stagnation_analysis.csv",
    index=False
)


# Department-wise role stagnation
department_stagnation = (
    df.groupby("Department", dropna=False)
    .agg(
        EmployeeCount=("Department", "size"),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageYearsInCurrentRole=(
            "YearsInCurrentRole", "mean"
        ),
        HighStagnationEmployees=(
            "RoleStagnationCategory",
            lambda x: (x == "High Role Stagnation").sum()
        )
    )
    .reset_index()
)

department_stagnation.to_csv(
    REPORT_DIR / "department_role_stagnation.csv",
    index=False
)


# Job-role-wise role stagnation
role_stagnation = (
    df.groupby("JobRole", dropna=False)
    .agg(
        EmployeeCount=("JobRole", "size"),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageYearsInCurrentRole=(
            "YearsInCurrentRole", "mean"
        ),
        HighStagnationEmployees=(
            "RoleStagnationCategory",
            lambda x: (x == "High Role Stagnation").sum()
        )
    )
    .reset_index()
)

role_stagnation.to_csv(
    REPORT_DIR / "jobrole_role_stagnation.csv",
    index=False
)


# ============================================================
# 7. CAREER PROGRESSION BY JOB LEVEL
# ============================================================

joblevel_analysis = (
    df.groupby("JobLevel", dropna=False)
    .agg(
        EmployeeCount=("JobLevel", "size"),
        AverageCompanyTenure=(
            "YearsAtCompany", "mean"
        ),
        AverageYearsSincePromotion=(
            "YearsSinceLastPromotion", "mean"
        ),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageSalaryHike=(
            "PercentSalaryHike", "mean"
        ),
        AveragePerformanceRating=(
            "PerformanceRating", "mean"
        )
    )
    .reset_index()
)

joblevel_analysis.to_csv(
    REPORT_DIR / "joblevel_career_analysis.csv",
    index=False
)


# ============================================================
# 8. TRAINING AND CAREER PROGRESSION
# ============================================================

training_analysis = (
    df.groupby("TrainingNeedIndicator", dropna=False)
    .agg(
        EmployeeCount=("TrainingNeedIndicator", "size"),
        AverageTrainingSessions=(
            "TrainingTimesLastYear", "mean"
        ),
        AveragePromotionGap=(
            "PromotionGapRatio", "mean"
        ),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AveragePerformance=(
            "PerformanceRating", "mean"
        )
    )
    .reset_index()
)

training_analysis.to_csv(
    REPORT_DIR / "training_career_analysis.csv",
    index=False
)


# Training intensity by department
training_department = (
    df.groupby("Department", dropna=False)
    .agg(
        EmployeeCount=("Department", "size"),
        AverageTrainingSessions=(
            "TrainingTimesLastYear", "mean"
        ),
        AverageTrainingIntensity=(
            "TrainingIntensityScore", "mean"
        ),
        HighTrainingNeedEmployees=(
            "TrainingNeedIndicator",
            lambda x: (x == "High Training Need").sum()
        )
    )
    .reset_index()
)

training_department.to_csv(
    REPORT_DIR / "department_training_analysis.csv",
    index=False
)


# ============================================================
# 9. MANAGER CONTINUITY AND CAREER GROWTH
# ============================================================

manager_analysis = (
    df.groupby("ManagerStabilityCategory", dropna=False)
    .agg(
        EmployeeCount=("ManagerStabilityCategory", "size"),
        AverageManagerTenure=(
            "YearsWithCurrManager", "mean"
        ),
        AveragePromotionGap=(
            "PromotionGapRatio", "mean"
        ),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageCompanyTenure=(
            "YearsAtCompany", "mean"
        )
    )
    .reset_index()
)

manager_analysis.to_csv(
    REPORT_DIR / "manager_career_analysis.csv",
    index=False
)


# ============================================================
# 10. CAREER PROGRESSION AND ATTRITION
# ============================================================

# Attrition is used here for descriptive comparison only.
# It will not be used as a clustering input.

attrition_analysis = (
    df.groupby("Attrition", dropna=False)
    .agg(
        EmployeeCount=("Attrition", "size"),
        AveragePromotionGap=(
            "PromotionGapRatio", "mean"
        ),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageTrainingIntensity=(
            "TrainingIntensityScore", "mean"
        ),
        AverageManagerStability=(
            "ManagerStabilityIndicator", "mean"
        ),
        AverageYearsAtCompany=(
            "YearsAtCompany", "mean"
        ),
        AverageYearsSincePromotion=(
            "YearsSinceLastPromotion", "mean"
        )
    )
    .reset_index()
)

attrition_analysis.to_csv(
    REPORT_DIR / "career_progression_by_attrition.csv",
    index=False
)


# ============================================================
# 11. RETENTION OPPORTUNITY ANALYSIS
# ============================================================

retention_analysis = (
    df.groupby("RetentionOpportunitySignal", dropna=False)
    .agg(
        EmployeeCount=("RetentionOpportunitySignal", "size"),
        AveragePromotionGap=(
            "PromotionGapRatio", "mean"
        ),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageJobSatisfaction=(
            "JobSatisfaction", "mean"
        ),
        AverageEnvironmentSatisfaction=(
            "EnvironmentSatisfaction", "mean"
        ),
        AverageTrainingSessions=(
            "TrainingTimesLastYear", "mean"
        )
    )
    .reset_index()
)

retention_analysis.to_csv(
    REPORT_DIR / "retention_opportunity_analysis.csv",
    index=False
)


# ============================================================
# 12. CAREER STAGE ANALYSIS
# ============================================================

career_stage_analysis = (
    df.groupby("CareerStage", dropna=False)
    .agg(
        EmployeeCount=("CareerStage", "size"),
        AverageCompanyTenure=(
            "YearsAtCompany", "mean"
        ),
        AveragePromotionGap=(
            "PromotionGapRatio", "mean"
        ),
        AverageRoleStagnation=(
            "RoleStagnationIndex", "mean"
        ),
        AverageTrainingSessions=(
            "TrainingTimesLastYear", "mean"
        ),
        HighPromotionGapEmployees=(
            "PromotionGapCategory",
            lambda x: (x == "High Promotion Gap").sum()
        )
    )
    .reset_index()
)

career_stage_analysis.to_csv(
    REPORT_DIR / "career_stage_analysis.csv",
    index=False
)


# ============================================================
# 13. CORRELATION ANALYSIS
# ============================================================

correlation_columns = [
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "PerformanceRating",
    "PercentSalaryHike",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "TrainingIntensityScore",
    "ManagerStabilityIndicator",
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "WorkLifeBalance"
]

correlation_matrix = df[
    correlation_columns
].corr(method="spearman")

correlation_matrix.to_csv(
    REPORT_DIR / "career_correlation_matrix.csv"
)


# ============================================================
# 14. VISUALIZATION FUNCTION
# ============================================================

def save_bar_chart(
    data,
    x_column,
    y_column,
    title,
    xlabel,
    ylabel,
    filename,
    rotate=0
):

    plt.figure(figsize=(11, 6))

    plt.bar(
        data[x_column].astype(str),
        data[y_column]
    )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.xticks(rotation=rotate, ha="right")
    plt.tight_layout()

    plt.savefig(
        CHART_DIR / filename,
        dpi=300
    )

    plt.close()


# ============================================================
# 15. PROMOTION GAP CHARTS
# ============================================================

save_bar_chart(
    promotion_summary,
    "PromotionGapCategory",
    "EmployeeCount",
    "Employee Distribution by Promotion Gap",
    "Promotion Gap Category",
    "Number of Employees",
    "promotion_gap_distribution.png"
)

department_promotion_sorted = (
    department_promotion.sort_values(
        "AveragePromotionGapRatio",
        ascending=False
    )
)

save_bar_chart(
    department_promotion_sorted,
    "Department",
    "AveragePromotionGapRatio",
    "Average Promotion Gap Ratio by Department",
    "Department",
    "Average Promotion Gap Ratio",
    "promotion_gap_by_department.png"
)


# ============================================================
# 16. ROLE STAGNATION CHARTS
# ============================================================

save_bar_chart(
    stagnation_summary,
    "RoleStagnationCategory",
    "EmployeeCount",
    "Employee Distribution by Role Stagnation",
    "Role Stagnation Category",
    "Number of Employees",
    "role_stagnation_distribution.png"
)

role_stagnation_sorted = (
    role_stagnation.sort_values(
        "AverageRoleStagnation",
        ascending=False
    )
)

save_bar_chart(
    role_stagnation_sorted,
    "JobRole",
    "AverageRoleStagnation",
    "Role Stagnation by Job Role",
    "Job Role",
    "Average Role Stagnation Index",
    "role_stagnation_by_jobrole.png",
    rotate=35
)


# ============================================================
# 17. TRAINING CHART
# ============================================================

save_bar_chart(
    training_analysis,
    "TrainingNeedIndicator",
    "EmployeeCount",
    "Employee Distribution by Training Need",
    "Training Need",
    "Number of Employees",
    "training_need_distribution.png"
)


# ============================================================
# 18. MANAGER CONTINUITY CHART
# ============================================================

save_bar_chart(
    manager_analysis,
    "ManagerStabilityCategory",
    "AveragePromotionGap",
    "Promotion Gap by Manager Continuity",
    "Manager Continuity",
    "Average Promotion Gap Ratio",
    "manager_continuity_vs_promotion.png"
)


# ============================================================
# 19. CAREER STAGE CHART
# ============================================================

save_bar_chart(
    career_stage_analysis,
    "CareerStage",
    "EmployeeCount",
    "Employee Distribution by Career Stage",
    "Career Stage",
    "Number of Employees",
    "career_stage_distribution.png"
)


# ============================================================
# 20. CAREER PROGRESSION AND ATTRITION CHART
# ============================================================

attrition_plot = attrition_analysis.copy()

attrition_plot["Attrition"] = (
    attrition_plot["Attrition"].astype(str)
)

save_bar_chart(
    attrition_plot,
    "Attrition",
    "AveragePromotionGap",
    "Average Promotion Gap by Attrition Status",
    "Attrition Status",
    "Average Promotion Gap Ratio",
    "promotion_gap_by_attrition.png"
)


# ============================================================
# 21. CORRELATION HEATMAP
# ============================================================

correlation_values = correlation_matrix.values

plt.figure(figsize=(15, 12))

image = plt.imshow(
    correlation_values,
    aspect="auto",
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.colorbar(image, label="Spearman Correlation")

plt.xticks(
    range(len(correlation_columns)),
    correlation_columns,
    rotation=90
)

plt.yticks(
    range(len(correlation_columns)),
    correlation_columns
)

plt.title("Career Progression Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "career_correlation_heatmap.png",
    dpi=300
)

plt.close()


# ============================================================
# 22. FINAL ANALYSIS SUMMARY
# ============================================================

summary = pd.DataFrame({
    "Metric": [
        "Total Employees",
        "High Promotion Gap Employees",
        "High Role Stagnation Employees",
        "High Training Need Employees",
        "Potential Retention Opportunity Employees"
    ],
    "Value": [
        len(df),
        int(
            (df["PromotionGapCategory"]
             == "High Promotion Gap").sum()
        ),
        int(
            (df["RoleStagnationCategory"]
             == "High Role Stagnation").sum()
        ),
        int(
            (df["TrainingNeedIndicator"]
             == "High Training Need").sum()
        ),
        int(
            (df["RetentionOpportunitySignal"]
             == "Potential Opportunity").sum()
        )
    ]
})

summary.to_csv(
    REPORT_DIR / "career_progression_summary.csv",
    index=False
)


# ============================================================
# 23. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("PHASE 5 COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nTotal employees analyzed:", len(df))

print("\nCareer progression summary:")
print(summary.to_string(index=False))

print("\nReports saved in:")
print(REPORT_DIR)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nPlease review the generated reports.")

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler


# ============================================================
# PHASE 6: CAREER PATH CLUSTERING
# ============================================================

warnings.filterwarnings("ignore", category=FutureWarning)

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "outputs"
    / "feature_engineering"
    / "employee_data_with_features.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "career_path_clustering"
CHART_DIR = OUTPUT_DIR / "charts"
REPORT_DIR = OUTPUT_DIR / "reports"

CHART_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PHASE 6: CAREER PATH CLUSTERING")
print("=" * 65)

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

print(f"\nInput dataset shape: {df.shape}")


# ------------------------------------------------------------
# 2. SELECT CAREER-RELATED FEATURES
# ------------------------------------------------------------

# Attrition is deliberately excluded from clustering.
# It may be examined after clustering for descriptive analysis.

feature_columns = [
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "JobLevel",
    "TrainingTimesLastYear",
    "PercentSalaryHike",
    "PerformanceRating"
]

missing_columns = [
    col for col in feature_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required clustering columns are missing: {missing_columns}"
    )

X = df[feature_columns].copy()

# Convert values to numeric and replace infinite values.
for col in feature_columns:
    X[col] = pd.to_numeric(X[col], errors="coerce")

X = X.replace([np.inf, -np.inf], np.nan)

if X.isna().all().any():
    all_missing = X.columns[X.isna().all()].tolist()
    raise ValueError(
        f"These clustering features contain no usable values: {all_missing}"
    )


# ------------------------------------------------------------
# 3. HANDLE MISSING VALUES AND SCALE FEATURES
# ------------------------------------------------------------

imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

print(f"Clustering features selected: {len(feature_columns)}")
print(f"Records used for clustering: {X_scaled.shape[0]}")
print("Missing values handled using median imputation.")
print("Numerical features standardized successfully.")


# Save the feature list and preprocessing details.
pd.DataFrame({
    "Clustering_Feature": feature_columns
}).to_csv(
    REPORT_DIR / "clustering_features.csv",
    index=False
)


# ------------------------------------------------------------
# 4. EVALUATE K-MEANS FOR DIFFERENT K VALUES
# ------------------------------------------------------------

k_values = range(2, 9)

inertia_values = []
silhouette_values = []

print("\nEvaluating K-Means cluster counts...")

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    labels = model.fit_predict(X_scaled)

    inertia_values.append(model.inertia_)

    score = silhouette_score(
        X_scaled,
        labels
    )

    silhouette_values.append(score)

    print(
        f"K = {k} | "
        f"Inertia = {model.inertia_:.2f} | "
        f"Silhouette Score = {score:.4f}"
    )


# Save evaluation metrics.
kmeans_metrics = pd.DataFrame({
    "Number_of_Clusters": list(k_values),
    "Inertia": inertia_values,
    "Silhouette_Score": silhouette_values
})

kmeans_metrics.to_csv(
    REPORT_DIR / "kmeans_evaluation_metrics.csv",
    index=False
)


# ------------------------------------------------------------
# 5. SELECT BEST K USING SILHOUETTE SCORE
# ------------------------------------------------------------

best_index = int(np.argmax(silhouette_values))
best_k = list(k_values)[best_index]
best_silhouette = silhouette_values[best_index]

print(f"\nSelected number of clusters: {best_k}")
print(f"Best silhouette score: {best_silhouette:.4f}")


# ------------------------------------------------------------
# 6. PLOT ELBOW CURVE
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.plot(
    list(k_values),
    inertia_values,
    marker="o"
)

plt.title("K-Means Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.xticks(list(k_values))
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "kmeans_elbow_curve.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 7. PLOT SILHOUETTE SCORES
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.plot(
    list(k_values),
    silhouette_values,
    marker="o"
)

plt.title("K-Means Silhouette Score")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.xticks(list(k_values))
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "kmeans_silhouette_scores.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 8. FINAL K-MEANS MODEL
# ------------------------------------------------------------

kmeans_model = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=20
)

kmeans_labels = kmeans_model.fit_predict(X_scaled)

# Cluster labels are identifiers, not rankings.
clustered_df = df.copy()

clustered_df.insert(
    0,
    "EmployeeRecordID",
    range(1, len(clustered_df) + 1)
)

clustered_df["CareerCluster"] = kmeans_labels

print("\nK-Means clustering completed.")


# ------------------------------------------------------------
# 9. CLUSTER SIZE ANALYSIS
# ------------------------------------------------------------

cluster_sizes = (
    clustered_df["CareerCluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_sizes.columns = [
    "CareerCluster",
    "EmployeeCount"
]

cluster_sizes["Percentage"] = (
    cluster_sizes["EmployeeCount"]
    / len(clustered_df)
    * 100
)

cluster_sizes.to_csv(
    REPORT_DIR / "cluster_size_distribution.csv",
    index=False
)


# ------------------------------------------------------------
# 10. CLUSTER FEATURE PROFILES
# ------------------------------------------------------------

cluster_profiles = (
    clustered_df
    .groupby("CareerCluster")[feature_columns]
    .mean()
    .round(2)
)

cluster_profiles.insert(
    0,
    "EmployeeCount",
    clustered_df.groupby("CareerCluster").size()
)

cluster_profiles.to_csv(
    REPORT_DIR / "cluster_feature_profiles.csv"
)


# ------------------------------------------------------------
# 11. POST-CLUSTERING ATTRITION COMPARISON
# ------------------------------------------------------------

# Attrition is used only to describe the resulting clusters.
# It is not used to fit either clustering model.

if "Attrition" in clustered_df.columns:

    attrition_profile = (
        clustered_df
        .groupby("CareerCluster")["Attrition"]
        .agg(
            EmployeeCount="count",
            AttritionRate="mean"
        )
        .reset_index()
    )

    attrition_profile["AttritionRate"] *= 100
    attrition_profile["AttritionRate"] = (
        attrition_profile["AttritionRate"].round(2)
    )

    attrition_profile.to_csv(
        REPORT_DIR / "cluster_attrition_comparison.csv",
        index=False
    )


# ------------------------------------------------------------
# 12. CATEGORICAL CAREER PROFILE
# ------------------------------------------------------------

categorical_columns = [
    "CareerStage",
    "PromotionGapCategory",
    "RoleStagnationCategory",
    "TrainingNeedIndicator",
    "ManagerStabilityCategory",
    "RetentionOpportunitySignal"
]

available_categorical = [
    col for col in categorical_columns if col in clustered_df.columns
]

categorical_results = []

for col in available_categorical:

    profile = (
        clustered_df
        .groupby(["CareerCluster", col], dropna=False)
        .size()
        .reset_index(name="EmployeeCount")
    )

    profile["PercentageWithinCluster"] = (
        profile["EmployeeCount"]
        / profile.groupby("CareerCluster")["EmployeeCount"]
        .transform("sum")
        * 100
    )

    profile["Feature"] = col
    profile = profile.rename(columns={col: "Category"})

    categorical_results.append(profile)

if categorical_results:

    categorical_profile = pd.concat(
        categorical_results,
        ignore_index=True
    )

    categorical_profile.to_csv(
        REPORT_DIR / "cluster_categorical_profiles.csv",
        index=False
    )


# ------------------------------------------------------------
# 13. HIERARCHICAL CLUSTERING VALIDATION
# ------------------------------------------------------------

print("\nRunning Hierarchical clustering validation...")

hierarchical_model = AgglomerativeClustering(
    n_clusters=best_k,
    linkage="ward"
)

hierarchical_labels = hierarchical_model.fit_predict(X_scaled)

hierarchical_silhouette = silhouette_score(
    X_scaled,
    hierarchical_labels
)

agreement_score = adjusted_rand_score(
    kmeans_labels,
    hierarchical_labels
)

validation_results = pd.DataFrame({
    "Method": [
        "K-Means",
        "Hierarchical (Ward)"
    ],
    "Number_of_Clusters": [
        best_k,
        best_k
    ],
    "Silhouette_Score": [
        best_silhouette,
        hierarchical_silhouette
    ]
})

validation_results.to_csv(
    REPORT_DIR / "clustering_validation_metrics.csv",
    index=False
)

pd.DataFrame({
    "EmployeeRecordID": range(1, len(df) + 1),
    "KMeansCluster": kmeans_labels,
    "HierarchicalCluster": hierarchical_labels
}).to_csv(
    REPORT_DIR / "hierarchical_cluster_comparison.csv",
    index=False
)

print(f"K-Means silhouette score: {best_silhouette:.4f}")
print(
    "Hierarchical silhouette score: "
    f"{hierarchical_silhouette:.4f}"
)
print(f"Adjusted Rand Index: {agreement_score:.4f}")


# ------------------------------------------------------------
# 14. PCA VISUALIZATION
# ------------------------------------------------------------

pca = PCA(n_components=2, random_state=42)

pca_coordinates = pca.fit_transform(X_scaled)

clustered_df["PCA1"] = pca_coordinates[:, 0]
clustered_df["PCA2"] = pca_coordinates[:, 1]

explained_variance = pca.explained_variance_ratio_.sum() * 100

plt.figure(figsize=(10, 7))

scatter = plt.scatter(
    clustered_df["PCA1"],
    clustered_df["PCA2"],
    c=clustered_df["CareerCluster"],
    cmap="viridis",
    alpha=0.7,
    s=35
)

plt.title("Employee Career Path Clusters (PCA)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(scatter, label="Career Cluster")
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "career_clusters_pca.png",
    dpi=300
)

plt.close()

print(
    f"PCA explained variance (2 components): "
    f"{explained_variance:.2f}%"
)


# ------------------------------------------------------------
# 15. SAVE FINAL EMPLOYEE CLUSTER DATA
# ------------------------------------------------------------

clustered_df.to_csv(
    OUTPUT_DIR / "employee_career_clusters.csv",
    index=False
)


# ------------------------------------------------------------
# 16. SAVE PHASE SUMMARY
# ------------------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Employees",
        "Clustering Features",
        "Selected Number of Clusters",
        "K-Means Silhouette Score",
        "Hierarchical Silhouette Score",
        "Adjusted Rand Index",
        "PCA Explained Variance (%)"
    ],
    "Value": [
        len(clustered_df),
        len(feature_columns),
        best_k,
        round(best_silhouette, 4),
        round(hierarchical_silhouette, 4),
        round(agreement_score, 4),
        round(explained_variance, 2)
    ]
})

summary.to_csv(
    REPORT_DIR / "career_clustering_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 17. FINAL CONSOLE OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PHASE 6 COMPLETED SUCCESSFULLY")
print("=" * 65)

print(f"Total employees clustered: {len(clustered_df)}")
print(f"Selected clusters: {best_k}")

print("\nCluster sizes:")
print(cluster_sizes.to_string(index=False))

print("\nCluster feature profiles:")
print(cluster_profiles.to_string())

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nReports saved in:")
print(REPORT_DIR)

print("\nNext phase: Promotion Gap Scoring and Retention Opportunity Analysis")

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PHASE 7: PROMOTION GAP SCORING AND RETENTION OPPORTUNITY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "outputs"
    / "career_path_clustering"
    / "employee_career_clusters.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "promotion_gap_scoring"
REPORT_DIR = OUTPUT_DIR / "reports"
CHART_DIR = OUTPUT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PHASE 7: PROMOTION GAP SCORING AND RETENTION OPPORTUNITY")
print("=" * 65)

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

print(f"\nDataset loaded successfully: {df.shape}")


# ------------------------------------------------------------
# 2. VALIDATE REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = [
    "CareerCluster",
    "YearsAtCompany",
    "YearsSinceLastPromotion",
    "YearsInCurrentRole",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "TrainingNeedIndicator",
    "ManagerStabilityIndicator",
    "JobSatisfaction",
    "JobInvolvement",
    "Department",
    "JobRole"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

numeric_columns = [
    "YearsAtCompany",
    "YearsSinceLastPromotion",
    "YearsInCurrentRole",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "ManagerStabilityIndicator",
    "JobSatisfaction",
    "JobInvolvement"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_columns] = df[numeric_columns].replace(
    [np.inf, -np.inf],
    np.nan
)

if df["CareerCluster"].isna().any():
    raise ValueError("CareerCluster contains missing values.")

# The Phase 6 record ID is a generated row number, not a real employee ID.
if "EmployeeRecordID" not in df.columns:
    df.insert(0, "EmployeeRecordID", range(1, len(df) + 1))


# ------------------------------------------------------------
# 3. DEFINE SCORING RULES
# ------------------------------------------------------------

# These thresholds are exploratory and should be reviewed
# with HR stakeholders before any real-world application.

def promotion_component(row):

    company_years = row["YearsAtCompany"]
    promotion_years = row["YearsSinceLastPromotion"]

    if pd.isna(company_years) or company_years <= 0:
        return np.nan

    if pd.isna(promotion_years):
        return np.nan

    if promotion_years >= 5:
        return 100
    elif promotion_years >= 3:
        return 60
    else:
        return 20


def stagnation_component(value):

    if pd.isna(value):
        return np.nan

    if value >= 0.80:
        return 100
    elif value >= 0.60:
        return 60
    else:
        return 20


df["PromotionGapComponent"] = df.apply(
    promotion_component,
    axis=1
)

df["RoleStagnationComponent"] = df[
    "RoleStagnationIndex"
].apply(stagnation_component)

# Promotion gap receives 60% weight.
# Role stagnation receives 40% weight.
df["PromotionGapRiskScore"] = (
    df["PromotionGapComponent"] * 0.60
    + df["RoleStagnationComponent"] * 0.40
)


# ------------------------------------------------------------
# 4. PROMOTION GAP RISK CATEGORY
# ------------------------------------------------------------

def classify_promotion_risk(row):

    if (
        pd.isna(row["PromotionGapRiskScore"])
        or row["YearsAtCompany"] <= 0
    ):
        return "Not Applicable"

    score = row["PromotionGapRiskScore"]

    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


df["PromotionGapRiskCategory"] = df.apply(
    classify_promotion_risk,
    axis=1
)


# ------------------------------------------------------------
# 5. TRAINING NEED INDICATOR
# ------------------------------------------------------------

df["TrainingNeedIndicator"] = (
    df["TrainingNeedIndicator"]
    .fillna("Not Assessed")
    .astype(str)
)

# Preserve the feature-engineering indicator rather than
# inventing a new training classification.


# ------------------------------------------------------------
# 6. MANAGER STABILITY IMPACT
# ------------------------------------------------------------

def classify_manager_stability(value):

    if pd.isna(value):
        return "Not Assessed"

    if value >= 0.80:
        return "High Continuity"
    elif value >= 0.40:
        return "Moderate Continuity"
    else:
        return "Low Continuity"


df["ManagerStabilityImpact"] = (
    df["ManagerStabilityIndicator"]
    .apply(classify_manager_stability)
)


# ------------------------------------------------------------
# 7. RETENTION OPPORTUNITY INDEX
# ------------------------------------------------------------

# Job satisfaction and job involvement are used as limited
# engagement proxies. They are not direct measures of intent
# to stay or leave.

def engagement_score(value):

    if pd.isna(value):
        return np.nan

    # Map the 1-4 scale to 0-100.
    return ((value - 1) / 3) * 100


df["JobSatisfactionScore"] = (
    df["JobSatisfaction"].apply(engagement_score)
)

df["JobInvolvementScore"] = (
    df["JobInvolvement"].apply(engagement_score)
)

df["EngagementProxyScore"] = df[
    ["JobSatisfactionScore", "JobInvolvementScore"]
].mean(axis=1)

# Career progression risk contributes 70%.
# Engagement proxy contributes 30%.
df["RetentionOpportunityIndex"] = (
    df["PromotionGapRiskScore"] * 0.70
    + df["EngagementProxyScore"] * 0.30
)


def classify_retention_opportunity(row):

    career_score = row["PromotionGapRiskScore"]
    engagement = row["EngagementProxyScore"]
    opportunity_score = row["RetentionOpportunityIndex"]

    if pd.isna(career_score) or pd.isna(engagement):
        return "Insufficient Data"

    # Require both a meaningful career signal and
    # a reasonable engagement proxy.
    if career_score < 50 or engagement < 50:
        return "No Immediate Opportunity Signal"

    if opportunity_score >= 70:
        return "High Opportunity"

    elif opportunity_score >= 55:
        return "Medium Opportunity"

    return "Low Opportunity"


df["RetentionOpportunityCategory"] = df.apply(
    classify_retention_opportunity,
    axis=1
)


# ------------------------------------------------------------
# 8. EMPLOYEE-LEVEL RECOMMENDATION
# ------------------------------------------------------------

def generate_recommendation(row):

    recommendations = []

    if row["PromotionGapRiskCategory"] == "High":
        recommendations.append(
            "Review promotion eligibility and career progression"
        )

    if row["RoleStagnationComponent"] == 100:
        recommendations.append(
            "Discuss role rotation or expanded responsibilities"
        )

    if row["TrainingNeedIndicator"] == "High":
        recommendations.append(
            "Assess targeted training and development"
        )

    if row["ManagerStabilityImpact"] == "Low Continuity":
        recommendations.append(
            "Review manager support and reporting continuity"
        )

    if not recommendations:
        recommendations.append(
            "Continue regular career development review"
        )

    return "; ".join(recommendations)


df["RecommendedIntervention"] = df.apply(
    generate_recommendation,
    axis=1
)


# ------------------------------------------------------------
# 9. OVERALL SCORE DISTRIBUTION
# ------------------------------------------------------------

risk_distribution = (
    df["PromotionGapRiskCategory"]
    .value_counts()
    .rename_axis("RiskCategory")
    .reset_index(name="EmployeeCount")
)

risk_distribution["Percentage"] = (
    risk_distribution["EmployeeCount"]
    / len(df) * 100
)

risk_distribution.to_csv(
    REPORT_DIR / "promotion_gap_risk_distribution.csv",
    index=False
)


retention_distribution = (
    df["RetentionOpportunityCategory"]
    .value_counts()
    .rename_axis("OpportunityCategory")
    .reset_index(name="EmployeeCount")
)

retention_distribution["Percentage"] = (
    retention_distribution["EmployeeCount"]
    / len(df) * 100
)

retention_distribution.to_csv(
    REPORT_DIR / "retention_opportunity_distribution.csv",
    index=False
)


# ------------------------------------------------------------
# 10. DEPARTMENT-WISE ANALYSIS
# ------------------------------------------------------------

department_analysis = (
    df.groupby("Department")
    .agg(
        EmployeeCount=("EmployeeRecordID", "count"),
        AveragePromotionRisk=("PromotionGapRiskScore", "mean"),
        AverageRetentionOpportunity=(
            "RetentionOpportunityIndex", "mean"
        ),
        HighPromotionRiskEmployees=(
            "PromotionGapRiskCategory",
            lambda x: (x == "High").sum()
        ),
        HighRetentionOpportunityEmployees=(
            "RetentionOpportunityCategory",
            lambda x: (x == "High Opportunity").sum()
        )
    )
    .reset_index()
)

department_analysis = department_analysis.round(2)

department_analysis.to_csv(
    REPORT_DIR / "department_risk_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 11. JOB-ROLE-WISE ANALYSIS
# ------------------------------------------------------------

jobrole_analysis = (
    df.groupby("JobRole")
    .agg(
        EmployeeCount=("EmployeeRecordID", "count"),
        AveragePromotionRisk=("PromotionGapRiskScore", "mean"),
        AverageRetentionOpportunity=(
            "RetentionOpportunityIndex", "mean"
        ),
        HighPromotionRiskEmployees=(
            "PromotionGapRiskCategory",
            lambda x: (x == "High").sum()
        ),
        HighRetentionOpportunityEmployees=(
            "RetentionOpportunityCategory",
            lambda x: (x == "High Opportunity").sum()
        )
    )
    .reset_index()
)

jobrole_analysis = jobrole_analysis.round(2)

jobrole_analysis.to_csv(
    REPORT_DIR / "jobrole_risk_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 12. CLUSTER-WISE ANALYSIS
# ------------------------------------------------------------

cluster_analysis = (
    df.groupby("CareerCluster")
    .agg(
        EmployeeCount=("EmployeeRecordID", "count"),
        AveragePromotionRisk=("PromotionGapRiskScore", "mean"),
        AverageRetentionOpportunity=(
            "RetentionOpportunityIndex", "mean"
        ),
        HighPromotionRiskEmployees=(
            "PromotionGapRiskCategory",
            lambda x: (x == "High").sum()
        ),
        HighRetentionOpportunityEmployees=(
            "RetentionOpportunityCategory",
            lambda x: (x == "High Opportunity").sum()
        )
    )
    .reset_index()
)

cluster_analysis = cluster_analysis.round(2)

cluster_analysis.to_csv(
    REPORT_DIR / "cluster_risk_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 13. PROMOTION RISK CROSS-TABULATIONS
# ------------------------------------------------------------

department_risk_crosstab = pd.crosstab(
    df["Department"],
    df["PromotionGapRiskCategory"]
)

department_risk_crosstab.to_csv(
    REPORT_DIR / "department_promotion_risk_crosstab.csv"
)


jobrole_risk_crosstab = pd.crosstab(
    df["JobRole"],
    df["PromotionGapRiskCategory"]
)

jobrole_risk_crosstab.to_csv(
    REPORT_DIR / "jobrole_promotion_risk_crosstab.csv"
)


cluster_risk_crosstab = pd.crosstab(
    df["CareerCluster"],
    df["PromotionGapRiskCategory"]
)

cluster_risk_crosstab.to_csv(
    REPORT_DIR / "cluster_promotion_risk_crosstab.csv"
)


# ------------------------------------------------------------
# 14. RETENTION OPPORTUNITY EMPLOYEE LIST
# ------------------------------------------------------------

opportunity_employees = df[
    df["RetentionOpportunityCategory"].isin(
        ["High Opportunity", "Medium Opportunity"]
    )
].copy()

opportunity_employees = opportunity_employees.sort_values(
    by="RetentionOpportunityIndex",
    ascending=False
)

employee_columns = [
    "EmployeeRecordID",
    "CareerCluster",
    "Department",
    "JobRole",
    "CareerStage",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "PromotionGapRiskScore",
    "PromotionGapRiskCategory",
    "EngagementProxyScore",
    "RetentionOpportunityIndex",
    "RetentionOpportunityCategory",
    "TrainingNeedIndicator",
    "ManagerStabilityImpact",
    "RecommendedIntervention"
]

employee_columns = [
    col for col in employee_columns if col in df.columns
]

opportunity_employees[employee_columns].to_csv(
    REPORT_DIR / "retention_opportunity_employee_list.csv",
    index=False
)


# ------------------------------------------------------------
# 15. TRAINING AND MANAGER STABILITY REPORTS
# ------------------------------------------------------------

training_analysis = (
    df.groupby("TrainingNeedIndicator")
    .agg(
        EmployeeCount=("EmployeeRecordID", "count"),
        AveragePromotionRisk=("PromotionGapRiskScore", "mean"),
        AverageRetentionOpportunity=(
            "RetentionOpportunityIndex", "mean"
        )
    )
    .reset_index()
    .round(2)
)

training_analysis.to_csv(
    REPORT_DIR / "training_need_analysis.csv",
    index=False
)


manager_analysis = (
    df.groupby("ManagerStabilityImpact")
    .agg(
        EmployeeCount=("EmployeeRecordID", "count"),
        AveragePromotionRisk=("PromotionGapRiskScore", "mean"),
        AverageRetentionOpportunity=(
            "RetentionOpportunityIndex", "mean"
        )
    )
    .reset_index()
    .round(2)
)

manager_analysis.to_csv(
    REPORT_DIR / "manager_stability_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 16. CHARTS
# ------------------------------------------------------------

# Promotion risk distribution
plt.figure(figsize=(9, 6))

sns.countplot(
    data=df,
    x="PromotionGapRiskCategory",
    order=["Low", "Medium", "High", "Not Applicable"]
)

plt.title("Promotion Gap Risk Distribution")
plt.xlabel("Promotion Gap Risk")
plt.ylabel("Number of Employees")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "promotion_gap_risk_distribution.png",
    dpi=300
)

plt.close()


# Retention opportunity distribution
plt.figure(figsize=(11, 6))

sns.countplot(
    data=df,
    x="RetentionOpportunityCategory",
    order=[
        "High Opportunity",
        "Medium Opportunity",
        "Low Opportunity",
        "No Immediate Opportunity Signal",
        "Insufficient Data"
    ]
)

plt.title("Retention Opportunity Distribution")
plt.xlabel("Retention Opportunity Category")
plt.ylabel("Number of Employees")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "retention_opportunity_distribution.png",
    dpi=300
)

plt.close()


# Average risk by department
plt.figure(figsize=(10, 6))

sns.barplot(
    data=department_analysis,
    x="Department",
    y="AveragePromotionRisk"
)

plt.title("Average Promotion Gap Risk by Department")
plt.xlabel("Department")
plt.ylabel("Average Promotion Gap Risk Score")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "promotion_risk_by_department.png",
    dpi=300
)

plt.close()


# Average risk by job role
plt.figure(figsize=(12, 7))

sns.barplot(
    data=jobrole_analysis,
    x="AveragePromotionRisk",
    y="JobRole"
)

plt.title("Average Promotion Gap Risk by Job Role")
plt.xlabel("Average Promotion Gap Risk Score")
plt.ylabel("Job Role")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "promotion_risk_by_jobrole.png",
    dpi=300
)

plt.close()


# Cluster versus promotion risk
plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="CareerCluster",
    hue="PromotionGapRiskCategory",
    hue_order=["Low", "Medium", "High", "Not Applicable"]
)

plt.title("Promotion Gap Risk Across Career Clusters")
plt.xlabel("Career Cluster")
plt.ylabel("Number of Employees")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "cluster_promotion_risk.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 17. SAVE FINAL EMPLOYEE DATA
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_DIR / "employee_promotion_retention_scores.csv",
    index=False
)


# ------------------------------------------------------------
# 18. PHASE SUMMARY
# ------------------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Employees",
        "High Promotion Risk Employees",
        "Medium Promotion Risk Employees",
        "Low Promotion Risk Employees",
        "Not Applicable Promotion Risk Employees",
        "High Retention Opportunity Employees",
        "Medium Retention Opportunity Employees",
        "Employees in High or Medium Opportunity Groups",
        "Average Promotion Gap Risk Score",
        "Average Retention Opportunity Index"
    ],
    "Value": [
        len(df),
        (df["PromotionGapRiskCategory"] == "High").sum(),
        (df["PromotionGapRiskCategory"] == "Medium").sum(),
        (df["PromotionGapRiskCategory"] == "Low").sum(),
        (df["PromotionGapRiskCategory"] == "Not Applicable").sum(),
        (df["RetentionOpportunityCategory"] == "High Opportunity").sum(),
        (df["RetentionOpportunityCategory"] == "Medium Opportunity").sum(),
        len(opportunity_employees),
        round(df["PromotionGapRiskScore"].mean(), 2),
        round(df["RetentionOpportunityIndex"].mean(), 2)
    ]
})

summary.to_csv(
    REPORT_DIR / "phase7_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 19. FINAL CONSOLE OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PHASE 7 COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nPromotion Gap Risk Distribution:")
print(risk_distribution.to_string(index=False))

print("\nRetention Opportunity Distribution:")
print(retention_distribution.to_string(index=False))

print("\nDepartment Risk Analysis:")
print(department_analysis.to_string(index=False))

print("\nCluster Risk Analysis:")
print(cluster_analysis.to_string(index=False))

print("\nHigh and Medium Retention Opportunity Employees:")
print(len(opportunity_employees))

print("\nAverage Promotion Gap Risk Score:")
print(round(df["PromotionGapRiskScore"].mean(), 2))

print("\nAverage Retention Opportunity Index:")
print(round(df["RetentionOpportunityIndex"].mean(), 2))

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nReports saved in:")
print(REPORT_DIR)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nNext phase: Streamlit Dashboard Development")

print("\n" + "=" * 65)




