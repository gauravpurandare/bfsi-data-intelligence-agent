
import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
#st.title("🏦 AI Banking Data Insight Agent")
st.set_page_config(
    page_title="BFSI Data Intelligence Agent",
    page_icon="🏦",
    layout="wide"
)
st.title("🏦 BFSI Data Intelligence Agent")
st.caption(
    "AI-powered Banking Data Analysis, Fraud Detection and Business Insights Platform"
)
st.success(
    "Upload a banking transaction dataset to perform data quality checks, fraud detection, business analysis and AI-assisted insights."
)
st.markdown(
    "Upload banking datasets and generate automated insights."
)

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Banking CSV File",
    type=["csv"]
)

# Main processing block
if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)
    st.success(
        f"Dataset loaded successfully. {len(df)} records available for analysis."
        )
    # =========================
    # Sidebar Filters
    # =========================

    st.sidebar.header("Filters")

    categorical_cols = df.select_dtypes(include='object').columns

    if len(categorical_cols) > 0:

        selected_col = st.sidebar.selectbox(
            "Select Category Column",
            categorical_cols
        )

        unique_values = list(df[selected_col].dropna().unique())
        # Add "All Data" at the beginning
        unique_values.insert(0, "All Data")

        selected_value = st.sidebar.selectbox(
            "Select Value",
            unique_values
        )

        if selected_value == "All Data":
            filtered_df = df
        else:
            filtered_df = df[df[selected_col] == selected_value]

    #else:
     #   filtered_df = df
    st.sidebar.write(
        f"Records selected: {len(filtered_df)}"
        )
    # =========================
    # Dataset Preview
    # =========================

    st.subheader("Dataset Preview")

    st.dataframe(filtered_df.head())

    # =========================
    # KPI Metrics
    # =========================

    st.subheader("Dataset Information")

    total_rows = filtered_df.shape[0]
    total_columns = filtered_df.shape[1]
    total_missing = filtered_df.isnull().sum().sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", total_rows)
    col2.metric("Columns", total_columns)
    col3.metric("Missing Values", total_missing)

    # =========================
    # Column Names
    # =========================

    st.subheader("Column Names")

    st.write(filtered_df.columns.tolist())

    # =========================
    # Missing Values
    # =========================

    st.subheader("Missing Values")

    missing_values = filtered_df.isnull().sum()

    st.dataframe(missing_values)

    # =========================
    # Duplicate Records
    # =========================

    st.subheader("Duplicate Records")

    duplicate_count = filtered_df.duplicated().sum()

    st.write(f"Duplicate Rows: {duplicate_count}")

    # =========================
    # Summary Statistics
    # =========================

    st.subheader("Summary Statistics")

    st.dataframe(filtered_df.describe())

    # =========================
    # Interactive Chart
    # =========================

    numeric_cols = filtered_df.select_dtypes(include='number').columns

    if len(numeric_cols) > 0:

        st.subheader("Interactive Chart")

        selected_numeric_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        fig = px.histogram(
            filtered_df,
            x=selected_numeric_col,
            title=f"Distribution of {selected_numeric_col}"
        )

        st.plotly_chart(fig)

    # =========================
    # Quick Business Insights
    # =========================

    st.subheader("Quick Business Insights")
    #### New code Start ####
     # AI-style Insight Generation

    insights = []

    # Missing values
    if total_missing > 0:
        insights.append(
            f"Data quality alert: {total_missing} missing values detected."
        )
    else:
        insights.append(
            "No missing values detected. Dataset quality looks good."
        )

    # Duplicate rows
    if duplicate_count > 0:
        insights.append(
         f"{duplicate_count} duplicate records found."
        )
    else:
        insights.append(
            "No duplicate records detected."
        )

    # Numeric analysis
    numeric_cols = filtered_df.select_dtypes(include='number').columns

    for col in numeric_cols:

        avg_value = filtered_df[col].mean()
        max_value = filtered_df[col].max()

        insights.append(
            f"For {col}, average value is {avg_value:.2f} and maximum value is {max_value:.2f}."
        )

    # Display insights
    for insight in insights:
        st.success(insight) 

    st.subheader("Executive Summary")

    st.info(
        f"""
        Dataset contains {filtered_df.shape[0]} records and
        {filtered_df.shape[1]} columns.

        Analysis indicates {duplicate_count} duplicate records
        and {total_missing} missing values.

        Review highlighted numerical trends and potential
        outlier transactions for further investigation.
        """
    )    
    #### New code End ####
    
    #total_missing = filtered_df.isnull().sum().sum()

   # st.write(f"""
    #- Total records analyzed: {filtered_df.shape[0]}
    #- Total columns analyzed: {filtered_df.shape[1]}
    #- Missing values detected: {total_missing}
    #- Duplicate records detected: {duplicate_count}
    #""")

    # =========================
    # Banking-Specific Logic
    # =========================

    if 'TransactionAmount' in filtered_df.columns:

        avg_amount = filtered_df['TransactionAmount'].mean()

        high_transactions = filtered_df[
            filtered_df['TransactionAmount'] > avg_amount
        ]

        st.subheader("High Value Transactions")

        st.write(
            f"Transactions above average amount: {len(high_transactions)}"
        )

        st.dataframe(high_transactions.head())

        ##### New code Start #####

        # =========================
        # Fraud Detection
        # =========================

        if 'TransactionAmount' in filtered_df.columns:

            st.subheader("🚨 Potential Fraud Detection")

            Q1 = filtered_df['TransactionAmount'].quantile(0.25)
            Q3 = filtered_df['TransactionAmount'].quantile(0.75)

            IQR = Q3 - Q1

            upper_limit = Q3 + (1.5 * IQR)

            suspicious_transactions = filtered_df[
            filtered_df['TransactionAmount'] > upper_limit
            ]
            ##### EXplainn suspicious transactions code
            st.subheader("🧠 Why Were These Transactions Flagged?")

            average_amount = filtered_df['TransactionAmount'].median()

            for index, row in suspicious_transactions.head(5).iterrows():

                multiplier = row['TransactionAmount'] / average_amount

                transaction_id = row.get(
                'TransactionID',
                f'Row {index}'
                )

                st.info(
                        f"""
                    Transaction ID: {transaction_id}

                    Transaction Amount: ${row['TransactionAmount']:,.2f}

                    Average Transaction Amount: ${average_amount:,.2f}

                    Reason:
                    This transaction is {multiplier:.1f} times higher than the average transaction value observed in the selected dataset.

                    Interpretation:
                    The transaction falls outside the normal transaction pattern and may represent high-value customer activity, an operational exception, or a transaction requiring additional review.
                """
                    )
            ##### Code ends
            st.metric(
            "Potentially Suspicious Transactions",
            len(suspicious_transactions)
            )

            if len(suspicious_transactions) > 0:

                st.warning(
             f"""
            {len(suspicious_transactions)} transaction(s) with value above ${upper_limit:,.2f} were flagged as potentially suspicious.

             Transactions exceed the expected range calculated from historical values
             and should be reviewed for potential fraud, operational exceptions,
            or high-value customer activity.

            This does not necessarily indicate fraud, but these transactions may warrant
            additional review by an analyst.
            """
                )

                suspicious_transactions = suspicious_transactions.copy()
                suspicious_transactions["Reason"] = (
                "Transaction amount significantly exceeds normal transaction pattern"
            )
                st.dataframe(suspicious_transactions)

            else:

                st.success(
                "No statistically unusual transactions detected."
            )
                if 'TransactionAmount' in filtered_df.columns:

                    fraud_percentage = (
                    len(suspicious_transactions)
                     / len(filtered_df)
                    ) * 100

                    st.subheader("Risk Assessment")

                    if fraud_percentage < 1:

                        st.success("Low Risk Dataset")

                    elif fraud_percentage < 5:

                        st.warning("Medium Risk Dataset")

                    else:

                        st.error("High Risk Dataset")
          ##### New code End #####

          # =========================
          # Data Assistant
          # =========================

        if uploaded_file: 
            st.subheader("🤖 Data Assistant")

            user_question = st.text_input(
            "Ask a question about the dataset"
            )
            if user_question:

                question = user_question.lower()

                if "rows" in question or "records" in question:

                    st.success(
                    f"The dataset contains {filtered_df.shape[0]} records."
                    )

                elif "columns" in question:

                    st.success(
                    f"The dataset contains {filtered_df.shape[1]} columns."
                    )

                elif "average transaction" in question:

                    if "TransactionAmount" in filtered_df.columns:

                        avg_amount = filtered_df["TransactionAmount"].mean()

                        st.success(
                        f"Average transaction amount is ${avg_amount:,.2f}"
                        )

                elif "highest transaction" in question:

                    if "TransactionAmount" in filtered_df.columns:

                        max_amount = filtered_df["TransactionAmount"].max()

                        st.success(
                        f"Highest transaction amount is ${max_amount:,.2f}"
                            )

                elif "missing values" in question:

                        missing_count = filtered_df.isnull().sum().sum()

                        st.success(
                        f"There are {missing_count} missing values."
                        )

                elif "duplicates" in question:

                        duplicate_count = filtered_df.duplicated().sum()

                        st.success(
                        f"There are {duplicate_count} duplicate records."
                    )

                else:

                    st.info(
                     """
                        I couldn't understand that question.

                        Try asking:
                        - How many records are there?
                        - What is the average transaction amount?
                        - What is the highest transaction?
                        - How many duplicates exist?
                    """
                        )
st.markdown("---")

st.caption(
    "BFSI Data Intelligence Agent | Built using Python, Pandas, Plotly and Streamlit"
)
