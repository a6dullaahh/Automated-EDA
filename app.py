import streamlit as st
from load import loader
from data_inspect import get_shape, get_dtypes, get_missing, get_summary, get_duplicates, get_column_types,get_unique_counts
from cleaning import drop_duplicates, handle_missing, convert_dtype, detect_outliers_iqr, remove_outliers_iqr,strip_whitespace
from analysis import(
    correlation_matrix,
    plot_correlation_heatmap,
    plot_histogram,
    plot_box,
    plot_bar_categorical,
    plot_scatter,
    plot_pairplot,
)

st.set_page_config(page_title="Automated EDA", layout="wide")
st.title("📊 Automated EDA App")

if "df" not in st.session_state:
    st.session_state.df = None
if "original_df" not in st.session_state:
    st.session_state.original_df = None

uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None and st.session_state.original_df is None:
    df_loaded = loader(uploaded_file)
    st.session_state.original_df = df_loaded
    st.session_state.df = df_loaded.copy()

if st.sidebar.button("🔄 Reset to original data") and st.session_state.original_df is not None:
    st.session_state.df = st.session_state.original_df.copy()
    st.rerun()

if st.session_state.original_df is None:
    st.info("Upload a CSV or Excel file from the sidebar to get started.")
    st.stop()

df = st.session_state.df

tab_overview, tab_inspect, tab_clean, tab_analysis = st.tabs(
    ["Overview", "Inspect", "Cleaning", "Analysis"]
)

# ---------------- Overview ----------------
with tab_overview:
    st.subheader("Data Preview")
    st.dataframe(df.head(50), use_container_width=True)

    rows, cols = get_shape(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", rows)
    c2.metric("Columns", cols)
    c3.metric("Duplicate rows", int(get_duplicates(df)))

# ---------------- Inspect ----------------
with tab_inspect:
    st.subheader("Column Types")
    st.dataframe(get_dtypes(df), use_container_width=True)

    st.subheader("Missing Values")
    st.dataframe(get_missing(df), use_container_width=True)

    st.subheader("Unique Value Counts")
    st.dataframe(get_unique_counts(df), use_container_width=True)

    st.subheader("Summary Statistics")
    st.dataframe(get_summary(df), use_container_width=True)

# ---------------- Cleaning ----------------
with tab_clean:
    st.subheader("Missing Value Handling")
    strategy = st.selectbox("Strategy", ["none", "drop", "mean", "median", "mode", "constant"])
    fill_value = st.text_input("Fill value (only for 'constant')", "0") if strategy == "constant" else None
    if st.button("Apply missing value strategy") and strategy != "none":
        st.session_state.df = handle_missing(df, strategy, fill_value)
        st.success(f"Applied strategy: {strategy}")
        st.rerun()

    st.divider()
    st.subheader("Duplicates")
    if st.button("Drop duplicate rows"):
        st.session_state.df = drop_duplicates(df)
        st.success("Duplicates removed")
        st.rerun()

    st.divider()
    st.subheader("Whitespace Cleanup")
    if st.button("Strip whitespace from text columns"):
        st.session_state.df = strip_whitespace(df)
        st.success("Whitespace stripped")
        st.rerun()

    st.divider()
    st.subheader("Outlier Removal (IQR method)")
    numeric_cols, _, _ = get_column_types(df)
    if numeric_cols:
        outlier_col = st.selectbox("Column", numeric_cols)
        outliers = detect_outliers_iqr(df, outlier_col)
        st.write(f"{len(outliers)} outlier rows detected")
        if st.button("Remove outliers"):
            st.session_state.df = remove_outliers_iqr(df, outlier_col)
            st.success("Outliers removed")
            st.rerun()
    else:
        st.caption("No numeric columns available.")

    st.divider()
    st.subheader("Convert Column Type")
    col_to_convert = st.selectbox("Column to convert", df.columns)
    new_type = st.selectbox("New type", ["str", "int64", "float64", "category", "datetime64[ns]"])
    if st.button("Convert type"):
        st.session_state.df = convert_dtype(df, col_to_convert, new_type)
        st.rerun()

    st.divider()
    st.download_button(
        "⬇️ Download current data as CSV",
        df.to_csv(index=False).encode("utf-8"),
        "cleaned_data.csv",
        "text/csv",
    )

# ---------------- Analysis ----------------
with tab_analysis:
    numeric_cols, categorical_cols, _ = get_column_types(df)

    if numeric_cols:
        st.subheader("Correlation Heatmap")
        st.pyplot(plot_correlation_heatmap(df))

        st.subheader("Distribution")
        hist_col = st.selectbox("Numeric column", numeric_cols, key="hist_col")
        st.pyplot(plot_histogram(df, hist_col))

        st.subheader("Scatter Plot")
        c1, c2, c3 = st.columns(3)
        x_col = c1.selectbox("X axis", numeric_cols, key="x_col")
        y_default = min(1, len(numeric_cols) - 1)
        y_col = c2.selectbox("Y axis", numeric_cols, index=y_default, key="y_col")
        color_col = c3.selectbox("Color (optional)", [None] + categorical_cols, key="color_col")
        st.pyplot(plot_scatter(df, x_col, y_col, color_col))
    else:
        st.caption("No numeric columns available for correlation/scatter analysis.")

    if categorical_cols:
        st.subheader("Category Counts")
        cat_col = st.selectbox("Categorical column", categorical_cols, key="cat_col")
        st.pyplot(plot_bar_categorical(df, cat_col))
    else:
        st.caption("No categorical columns available.")
