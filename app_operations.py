import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import streamlit as st
import numpy as np

@st.cache_data
def load_dataset(option):
    if option == "Iris Dataset":
        iris = load_iris(as_frame=True)
        df = pd.concat([iris.data, iris.target.rename("species")], axis=1)
    elif option == "Titanic Dataset":
        df = sns.load_dataset('titanic')
    elif option == "Penguins Dataset":
        df = sns.load_dataset('penguins')
    else:
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        else:
            df = None
    return df

# Displaying the welcome message to the user with the steps to get started with the dashboard
def display_welcome_message():
    st.title("📊 Data Analysis Dashboard")
    st.markdown("""
    ### 👋 Welcome to your Data Analysis Companion!
    
    This dashboard makes data analysis and visualization simple and intuitive.
    Follow these steps to get started:
    
    1. 📁 Choose a sample dataset or upload your own
    2. 🔍 Preview your data and check basic statistics
    3. 📈 Create beautiful visualizations with just a few clicks
    """)

# Setting up the sidebar with the dataset selection dropdown
def setup_sidebar():
    st.sidebar.header("🎯 Dataset Selection")
    return st.sidebar.selectbox(
        "Choose your dataset",
        ["Iris Dataset 🌸", "Titanic Dataset 🚢", "Penguins Dataset 🐧", "Upload Custom Dataset 📤"],
        help="Select a pre-loaded dataset or upload your own"
    )

# Getting the dataset name based on the user's choice for display purposes in the dashboard
def get_dataset_name(option):
    name_mapping = {
        "Iris": "Iris Dataset",
        "Titanic": "Titanic Dataset",
        "Penguins": "Penguins Dataset",
        "Upload": "Upload Custom Dataset"
    }
    first_word = option.split()[0]
    return name_mapping.get(first_word, first_word)

# Displaying the help section with a quick start guide, visualization types, tips, and troubleshooting information
def display_help_section():
    with st.sidebar.expander("📖 Help & Guide"):
        st.markdown("""
        ### 🚀 Quick Start Guide
        
        #### 📊 Available Datasets:
        - **Iris Dataset 🌸**: Flower measurements (ideal for classification)
        - **Titanic Dataset 🚢**: Passenger survival data
        - **Penguins Dataset 🐧**: Penguin measurements
        - **Custom Dataset 📤**: Your own CSV/Excel file
        
        #### 📈 Visualization Types:
        - **Scatter Plot**: Compare two variables
        - **Line Plot**: Show trends over time
        - **Histogram**: View data distribution
        - **Box Plot**: Identify outliers
        - **Heat Map**: Analyze correlations
        - **Pair Plot**: Multi-variable relationships
        - **Bar Plot**: Categorical data comparison
        - **Pie Chart**: Percentage breakdown
        
        #### 💡 Tips:
        - Clean your data before uploading
        - Remove missing values if possible
        - Use appropriate chart types for your data
        
        #### ⚠️ Troubleshooting:
        - File not loading? Check format (CSV/Excel)
        - Visualization empty? Check column selections
        - Strange results? Check for missing values
        """)

# Displaying the dataset preview with the first 10 rows of the dataset for a quick overview of the data structure and content 
def display_dataset_preview(df):
    st.write("## Dataset Preview")
    st.write("🔍 Previewing the first 10 rows of the dataset:")
    st.dataframe(df.head(10))

# Displaying basic statistics of the dataset including count, mean, standard deviation, minimum, maximum, etc. 
@st.cache_data
def display_basic_statistics(df):
    st.write("## Basic Statistics")
    st.write(df.describe())

def load_custom_file(file):
    """Load a custom file with proper error handling."""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            return None, "❌ Unsupported file format. Please upload a CSV or Excel file."
        
        # Basic validation
        if df.empty:
            return None, "❌ The uploaded file is empty."
        if df.shape[1] < 2:
            return None, "❌ The file must contain at least two columns for analysis."
            
        return df, None
    except Exception as e:
        return None, f"❌ Error reading file: {str(e)}"


def display_data_visualization(df):
    """Display visualizations with proper error handling and cleanup."""
    try:
        st.write("## Data Visualization")
        chart_type = st.selectbox("Select chart type",
                                  ["Scatter Plot", "Line Plot", "Histogram", "Box Plot", "Correlation Heatmap", "Bar Plot", "Pie Chart"])

        # Get numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found in the dataset.")
            return

        plt.figure(figsize=(10, 6))

        try:
            if chart_type == "Scatter Plot":
                if len(numeric_cols) < 2:
                    st.warning("Need at least two numeric columns for a scatter plot.")
                    return
                
                x_axis = st.selectbox("Select X-axis", numeric_cols)
                y_axis = st.selectbox("Select Y-axis", numeric_cols)
                
                sns.scatterplot(data=df, x=x_axis, y=y_axis)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title(f"Scatter Plot: {x_axis} vs {y_axis}")

            elif chart_type == "Line Plot":
                x_axis = st.selectbox("Select X-axis", df.columns)
                y_axis = st.selectbox("Select Y-axis", numeric_cols)
                
                sns.lineplot(data=df, x=x_axis, y=y_axis)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title(f"Line Plot: {y_axis} over {x_axis}")
                plt.xticks(rotation=45)

            elif chart_type == "Histogram":
                column = st.selectbox("Select column", numeric_cols)
                bins = st.slider("Number of bins", 5, 50, 20)
                
                sns.histplot(df[column], kde=True, bins=bins)
                plt.xlabel(column)
                plt.ylabel("Count")
                plt.title(f"Histogram of {column}")

            elif chart_type == "Box Plot":
                column = st.selectbox("Select column", numeric_cols)
                
                sns.boxplot(y=df[column])
                plt.ylabel(column)
                plt.title(f"Box Plot of {column}")

            elif chart_type == "Correlation Heatmap":
                numeric_df = df[numeric_cols]
                if numeric_df.shape[1] < 2:
                    st.warning("Need at least two numeric columns for a correlation heatmap.")
                    return
                
                sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
                plt.title("Correlation Heatmap")

            elif chart_type == "Bar Plot":
                x_axis = st.selectbox("Select X-axis (categories)", df.columns)
                y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols)
                
                sns.barplot(data=df, x=x_axis, y=y_axis)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title(f"Bar Plot: {y_axis} by {x_axis}")
                plt.xticks(rotation=45)

            elif chart_type == "Pie Chart":
                column = st.selectbox("Select column", categorical_cols if categorical_cols else df.columns)
                plt.pie(df[column].value_counts(), labels=df[column].value_counts().index, autopct='%1.1f%%')
                plt.title(f"Pie Chart of {column}")

            else:
                st.warning("Invalid chart type selected.")
                return
             
            st.pyplot(plt)
            plt.close()

            # Ensure cleanup even if there's an error in the visualization code 
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            plt.close()

    except Exception as e:
        st.error(f"Error in visualization module: {str(e)}")