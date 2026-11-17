
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# 2. PROJECT PATHS
# --------------------------------------------------


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "dataset" / "raw" / "telco.csv"

# Search for segmentation artifacts in both locations

REPORT_LOCATIONS = [
    PROJECT_ROOT / "reports",
    PROJECT_ROOT / "notebooks" / "reports"
]

SEGMENTATION_PATH = next(
    (
        folder / "customer_segmentation_results.csv"
        for folder in REPORT_LOCATIONS
        if (folder / "customer_segmentation_results.csv").exists()
    ),
    PROJECT_ROOT / "reports" / "customer_segmentation_results.csv"
)

CLUSTER_PROFILE_PATH = next(
    (
        folder / "cluster_profile_summary.csv"
        for folder in REPORT_LOCATIONS
        if (folder / "cluster_profile_summary.csv").exists()
    ),
    PROJECT_ROOT / "reports" / "cluster_profile_summary.csv"
)


# --------------------------------------------------
# 3. LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_segmentation():
    return pd.read_csv(SEGMENTATION_PATH)


@st.cache_data
def load_cluster_profile():
    return pd.read_csv(CLUSTER_PROFILE_PATH)


try:
    df = load_data()

except Exception as e:
    st.error(f"Dataset loading failed: {e}")
    st.stop()


# --------------------------------------------------
# 4. GLOBAL APPLICATION HEADER
# --------------------------------------------------

st.title("Customer Retention Intelligence Platform")

st.markdown(
    "An analytics-driven platform for customer churn "
    "prediction, segmentation and retention decision-making."
)

st.divider()


# --------------------------------------------------
# 5. NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Overview",
        "Churn Analysis",
        "Customer Segmentation",
        "Retention ROI Simulator"
    ]
)


# ==================================================
# PAGE 1: OVERVIEW
# ==================================================

if page == "Overview":

    st.header("Customer Business Overview")

    total_customers = len(df)

    churned_customers = (
        df["Churn Label"].eq("Yes").sum()
    )

    retained_customers = (
        df["Churn Label"].eq("No").sum()
    )

    churn_rate = (
        churned_customers / total_customers * 100
    )

    average_monthly_charge = (
        df["Monthly Charge"].mean()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Churned Customers",
        f"{churned_customers:,}"
    )

    col3.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

    col4.metric(
        "Avg Monthly Charge",
        f"${average_monthly_charge:.2f}"
    )

    st.divider()

    st.subheader("Welcome")

    st.write(
        "Explore customer behavior, identify churn risks "
        "and develop data-driven retention strategies."
    )

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# ==================================================
# PAGE 2: CHURN ANALYSIS
# ==================================================

elif page == "Churn Analysis":

    st.header("Customer Churn Analysis")

    st.markdown(
        "Understand customer retention patterns "
        "through churn distribution and business metrics."
    )

    # ----------------------------------------------
    # 2.1 CUSTOMER CHURN DISTRIBUTION
    # ----------------------------------------------

    st.subheader("Customer Churn Distribution")

    churn_distribution = (
        df["Churn Label"]
        .value_counts()
        .rename_axis("Customer Status")
        .reset_index(name="Customers")
    )

    st.bar_chart(
        churn_distribution,
        x="Customer Status",
        y="Customers",
        y_label="Number of Customers"
    )

    # ----------------------------------------------
    # 2.2 CUSTOMER CHURN KPIs
    # ----------------------------------------------

    churn_percentage = (
        df["Churn Label"]
        .value_counts(normalize=True) * 100
    )

    retained_customers = (
        df["Churn Label"].eq("No").sum()
    )

    churned_customers = (
        df["Churn Label"].eq("Yes").sum()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Retained Customers",
        f"{retained_customers:,}",
        f"{churn_percentage.get('No', 0):.2f}%"
    )

    col2.metric(
        "Churned Customers",
        f"{churned_customers:,}",
        f"{churn_percentage.get('Yes', 0):.2f}%",
        delta_color="inverse"
    )

    st.divider()

    # ----------------------------------------------
    # 2.3 CHURN RATE BY CONTRACT TYPE
    # ----------------------------------------------

    st.subheader("Churn Rate by Contract Type")

    contract_analysis = (
        df.assign(
            Churn_Flag=df["Churn Label"].eq("Yes")
        )
        .groupby("Contract")["Churn_Flag"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
        .rename("Churn Rate (%)")
        .reset_index()
    )

    st.bar_chart(
        contract_analysis,
        x="Contract",
        y="Churn Rate (%)",
        y_label="Churn Rate (%)"
    )

    st.dataframe(
        contract_analysis,
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------
    # 2.4 CHURN RATE BY CUSTOMER TENURE
    # ----------------------------------------------

    st.subheader("Churn Rate by Customer Tenure")

    tenure_bins = [0, 6, 12, 24, 48, 72]

    tenure_labels = [
        "0-6 Months",
        "7-12 Months",
        "13-24 Months",
        "25-48 Months",
        "49-72 Months"
    ]

    tenure_analysis = df.copy()

    tenure_analysis["Tenure Group"] = pd.cut(
        tenure_analysis["Tenure in Months"],
        bins=tenure_bins,
        labels=tenure_labels,
        include_lowest=True
    )

    churn_by_tenure = (
        tenure_analysis.assign(
            Churn_Flag=tenure_analysis["Churn Label"].eq("Yes")
        )
        .groupby(
            "Tenure Group",
            observed=False
        )["Churn_Flag"]
        .mean()
        .mul(100)
        .round(2)
        .rename("Churn Rate (%)")
        .reset_index()
    )

    st.bar_chart(
        churn_by_tenure,
        x="Tenure Group",
        y="Churn Rate (%)",
        y_label="Churn Rate (%)"
    )

    st.dataframe(
        churn_by_tenure,
        use_container_width=True
    )


# ==================================================
# PAGE 3: CUSTOMER SEGMENTATION
# ==================================================

elif page == "Customer Segmentation":

    st.header("Customer Segmentation")

    st.markdown(
        "Explore customer groups created using the "
        "KMeans clustering model."
    )

    if (
        SEGMENTATION_PATH.exists()
        and CLUSTER_PROFILE_PATH.exists()
    ):

        try:
            segmentation_df = load_segmentation()
            cluster_profile = load_cluster_profile()

            st.subheader("Customer Segment Overview")

            total_segmented = len(segmentation_df)

            total_segments = (
                segmentation_df["Customer Segment"].nunique()
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Segmented Customers",
                f"{total_segmented:,}"
            )

            col2.metric(
                "Customer Segments",
                total_segments
            )

            st.divider()

            st.subheader("Customer Distribution by Segment")

            segment_distribution = (
                segmentation_df["Customer Segment"]
                .value_counts()
                .rename_axis("Customer Segment")
                .reset_index(name="Customer Count")
            )

            st.bar_chart(
                segment_distribution,
                x="Customer Segment",
                y="Customer Count"
            )

            st.divider()

            st.subheader("Cluster Profile")

            st.dataframe(
                cluster_profile,
                use_container_width=True
            )

            st.subheader("Customer Segmentation Records")

            st.dataframe(
                segmentation_df.head(20),
                use_container_width=True
            )

        except Exception as e:
            st.error(
                f"Segmentation data loading failed: {e}"
            )

    else:

        st.warning(
            "Segmentation result files were not found. "
            "Please verify the exported CSV files in the reports folder."
        )


# ==================================================
# PAGE 4: RETENTION ROI SIMULATOR
# ==================================================


elif page == "Retention ROI Simulator":

    st.header("Retention ROI Simulator")

    st.markdown(
        "Estimate the financial impact of a customer retention campaign "
        "using adjustable business assumptions."
    )

    st.divider()

    # -----------------------------------------
    # CAMPAIGN INPUTS
    # -----------------------------------------

    st.subheader("Campaign Configuration")

    # Calculate churned customers locally
    churned_customers = int(
        df["Churn Label"].eq("Yes").sum()
    )

    col1, col2 = st.columns(2)

    with col1:
        target_customers = st.number_input(
            "Customers Targeted",
            min_value=1,
            max_value=len(df),
            value=min(churned_customers, len(df)),
            step=100
        )

        discount_percentage = st.slider(
            "Discount Offered (%)",
            min_value=0,
            max_value=50,
            value=10
        )

        discount_months = st.slider(
            "Discount Duration (Months)",
            min_value=1,
            max_value=12,
            value=3
        )

    with col2:
        expected_save_rate = st.slider(
            "Assumed Retention Success Rate (%)",
            min_value=1,
            max_value=100,
            value=20
        )

        retention_horizon = st.slider(
            "Revenue Projection (Months)",
            min_value=1,
            max_value=24,
            value=12
        )

        contact_cost = st.number_input(
            "Campaign Contact Cost per Customer ($)",
            min_value=0.0,
            value=2.0,
            step=0.5
        )

    # -----------------------------------------
    # ROI CALCULATIONS
    # -----------------------------------------

    average_charge = df["Monthly Charge"].mean()

    expected_saved = (
        target_customers * expected_save_rate / 100
    )

    discount_cost = (
        target_customers
        * average_charge
        * discount_percentage / 100
        * discount_months
    )

    contact_expense = target_customers * contact_cost

    total_campaign_cost = discount_cost + contact_expense

    revenue_preserved = (
        expected_saved
        * average_charge
        * retention_horizon
    )

    net_benefit = revenue_preserved - total_campaign_cost

    if total_campaign_cost > 0:
        roi = (
            net_benefit / total_campaign_cost
        ) * 100
    else:
        roi = 0

    # -----------------------------------------
    # BUSINESS RESULTS
    # -----------------------------------------

    st.divider()

    st.subheader("Campaign Financial Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Expected Customers Retained",
        f"{expected_saved:,.0f}"
    )

    col2.metric(
        "Estimated Revenue Preserved",
        f"${revenue_preserved:,.2f}"
    )

    col3.metric(
        "Total Campaign Cost",
        f"${total_campaign_cost:,.2f}"
    )

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        "Net Financial Benefit",
        f"${net_benefit:,.2f}"
    )

    col2.metric(
        "Estimated Campaign ROI",
        f"{roi:.2f}%"
    )

    # -----------------------------------------
    # BUSINESS INTERPRETATION
    # -----------------------------------------

    st.divider()

    st.subheader("Business Recommendation")

    if roi > 0:
        st.success(
            "The campaign shows a positive estimated financial return "
            "under the selected assumptions."
        )

    elif roi < 0:
        st.warning(
            "The campaign shows a negative estimated financial return. "
            "Consider revising the campaign assumptions."
        )

    else:
        st.info(
            "The campaign is estimated to break even."
        )

    # -----------------------------------------
    # TRANSPARENCY
    # -----------------------------------------

    st.divider()

    st.caption(
        "Note: This simulator uses user-defined retention assumptions "
        "and average monthly charges. It is an illustrative gross-revenue "
        "scenario, not a validated causal uplift prediction or guaranteed ROI. "
        "Discounts are assumed to apply to all targeted customers."
    )
