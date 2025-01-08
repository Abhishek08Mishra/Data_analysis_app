import streamlit as st

from app_operations import (
    load_dataset,
    load_custom_file,
    setup_sidebar,
    get_dataset_name,
    display_help_section,
    display_welcome_message,
    display_dataset_preview,
    display_basic_statistics,
    display_data_visualization
)

def main():
    try:
        st.set_page_config(
            page_title="Data Analysis Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        display_welcome_message()
        dataset_option = setup_sidebar()
        df = None
        error_message = None

        try:
            if "Upload" in dataset_option:
                uploaded_file = st.sidebar.file_uploader(
                    "📤 Upload your file",
                    type=["csv", "xlsx", "xls"],
                    help="Supported formats: CSV, Excel (.xlsx, .xls)"
                )
                if uploaded_file:
                    df, error_message = load_custom_file(uploaded_file)
            else:
                dataset_name = get_dataset_name(dataset_option)
                df = load_dataset(dataset_name)
                if df is None:
                    error_message = f"❌ Error loading {dataset_name}"

        except Exception as e:
            error_message = f"❌ Error loading dataset: {str(e)}"

        if error_message:
            st.error(error_message)
            return

        if df is not None:
            st.sidebar.header("🔧 Analysis Options")
            show_preview = st.sidebar.checkbox("📋 Show Dataset Preview", True)
            show_stats = st.sidebar.checkbox("📊 Show Basic Statistics", True)
            show_viz = st.sidebar.checkbox("📈 Show Data Visualization", True)

            if show_preview:
                with st.expander("📋 Dataset Preview", expanded=True):
                    display_dataset_preview(df)

            if show_stats:
                with st.expander("📊 Basic Statistics", expanded=True):
                    display_basic_statistics(df)

            if show_viz:
                with st.expander("📈 Data Visualization", expanded=True):
                    display_data_visualization(df)

            with st.sidebar.expander("ℹ️ Dataset Info"):
                st.write(f"🔢 Rows: {df.shape[0]}")
                st.write(f"📐 Columns: {df.shape[1]}")
                st.write("📋 Column Types:")
                st.write(df.dtypes)

            display_help_section()

        else:
            st.info("👆 Please select a dataset or upload your own file to begin the analysis.")

    except Exception as e:
        st.error(f"""
        ❌ An unexpected error occurred:
        ```python
        {str(e)}
        ```
        Please try refreshing the page or contact support if the problem persists.
        """)
        st.sidebar.error("⚠️ Error encountered. Check main window for details.")

if __name__ == "__main__":
    main()