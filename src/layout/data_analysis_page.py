import numpy as np
import pandas as pd
import streamlit as st
from io import StringIO
from pandas import DataFrame
import streamlit_antd_components as sac
from pygwalker.api.streamlit import StreamlitRenderer

from utils import ArcticOps


def data_analysis(analysis_options):
    
    arctic_ops = ArcticOps(
        temperature = analysis_options["model_parameters"]["temperature"],
        top_p = analysis_options["model_parameters"]["top_p"]
        )

    with st.container(border = True):
        uploaded_file = get_uploaded_file()
        col1, col2, col3 = st.columns([1, 1, 3])
        if uploaded_file:
            with col1:
                load_dataset_button = st.button(":arrow_up: Load Dataset", use_container_width = True)
                if load_dataset_button:
                    to_pop = ["data_insights_output", "visualization_insights", "visualization_markdown", "viz_insights_first"]
                    for key_to_pop in to_pop:
                        if st.session_state.get(key_to_pop):
                            st.session_state.pop(key_to_pop)
                    df = load_data_to_dataframe(uploaded_file)
                    st.session_state["dataframe"] = df
        else:
            with col1:
                if st.session_state.get("dataframe", None) is not None:
                    clear_data_button = st.button(":wastebasket: Clear Data", use_container_width = True)
                    if clear_data_button:
                        st.session_state.pop("dataframe")
                        st.rerun()

    if st.session_state.get("dataframe", None) is not None:
        df = st.session_state["dataframe"]
        if analysis_options["menu_selection"] == "Data Visualizations":
            display_data_viz_insights(df, arctic_ops)
                
        elif analysis_options["menu_selection"] == "Data Analysis":
            with st.container(border = True):
                display_data_analysis(analysis_options["analysis_options"], arctic_ops)


def get_uploaded_file():

    uploaded_file = st.file_uploader(
        label = "Upload your file here",
        type = "CSV",
        accept_multiple_files = False,
    )
    return(uploaded_file)


def load_data_to_dataframe(uploaded_file):

    df = pd.read_csv(uploaded_file)
    return(df)


def display_data_viz_insights(df, arctic_ops: ArcticOps):

    with st.container(border = True):
        pyg_app = StreamlitRenderer(df)
        pyg_app.explorer(default_tab = "data", height = 800)
        generate_viz_insights = st.button("Generate Visualization Insights")
        if generate_viz_insights:
            prompt = generate_viz_insights_prompt(df)
            response_markdown = ""
            with st.spinner("Generating ..."):
                response = arctic_ops.invoke_snowflake_arctic_simple(prompt)
                for item in response:
                    response_markdown += item
                st.session_state["visualization_insights"] = response
                st.session_state["visualization_markdown"] = response_markdown
                st.session_state["viz_insights_first"] = True
    
    if st.session_state.get("visualization_insights"):
        with st.container(border = True):
            st.subheader("Visualization Insights")
            if st.session_state.get("viz_insights_first", False): 
                st.write(st.session_state["visualization_markdown"])
                st.session_state["viz_insights_first"] = False
            else:
                st.markdown(st.session_state["visualization_markdown"])


def generate_viz_insights_prompt(df: pd.DataFrame) -> str:

    prompt = f"""   
    You are an expert in data analysis and data visualization. You have been provided with a data set in the form
    of a dataframe. You will be given the column names of the dataframe, the dtypes of the dataframe, a random sample
    of the dataframe, and the descriptive statistics of a dataframe. With these information propose a list of the five most 
    useful plots to gain insights from this dataset. For each plot specify which columns should be used and how the need to be
    modified if necessary.

    Dataframe Columns:
    {df.columns} 

    Dataframe Columns Dtypes:
    {df.dtypes}

    Dataframe Data Sample:
    {get_random_sample(df)}

    Dataframe Descriptive Statistics:
    {df.describe()}
    """

    return(prompt)


def generate_data_insights_prompt(df: pd.DataFrame) -> str:

    prompt = f"""   
    You are an expert in data and statistical analysis with a focus on extracting meaningful insights from datasets. 
    You will be provided with the following details of a dataframe:
    - Column names and data types.
    - A random sample of the dataframe.
    - Descriptive statistics of the dataframe.
    - The correlation matrix of the dataframe.

    Your task is to:
        1. Identify and isolate key characteristics of the dataset.
        2. Provide useful insights based on the data.
        3. Propose further analyses that could deepen the understanding of the data.
        4. Interpret the statistical and other data provided to derive meaningful conclusions.

    Data Sample:
    {get_random_sample(df)}

    Dataframe Information:
    {get_dataframe_info_as_dataframe(df)}

    Descriptive Statistics:
    {df.describe()}

    Correlation Matrix:
    {generate_correlation_matrix(df)}
    """

    return(prompt)


def display_data_analysis(analysis_options, arctic_ops):

    st.subheader("Data Insights")
    df = st.session_state["dataframe"]
    col1, col2 = st.columns([1, 1])
    with col1:
        if analysis_options["data_sample"]:
            with st.expander("**Data Sample**", expanded = True):
                st.write(get_random_sample(df))
    with col2:
        if analysis_options["data_summary"]:
            with st.expander("**Data Summary**", expanded = True):
                st.write(get_dataframe_info_as_dataframe(df))

    with col1:
        if analysis_options["descriptive_statistics"]:
            with st.expander("**Descriptive Statistics**", expanded = True):
                st.write(generate_descriptive_statistics(df))
    with col2:
        if analysis_options["correlation"]:
            with st.expander("**Pairwise correlation of columns**", expanded = True):
                st.write(generate_correlation_matrix(df))
            
    if analysis_options["data_insights"]:
        with st.expander("**Data Insights**", expanded = True):
            generate_data_insights(df, arctic_ops)


def get_random_sample(df: pd.DataFrame, sample_size: int = 10) -> pd.DataFrame:
    """
    Returns a random sample from the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to sample from.
        sample_size (int): The number of rows to return in the sample.

    Returns:
        pd.DataFrame: A DataFrame containing the random sample.
    """
    return df.sample(n=sample_size, random_state=np.random.randint(0, 10000))


def generate_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates descriptive statistics for the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to generate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the descriptive statistics.
    """
    return df.describe()


def get_dataframe_info_as_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the information summary of a pandas DataFrame as a new DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to get the info summary.

    Returns:
        pd.DataFrame: A DataFrame containing the information summary.
    """
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    
    # Parse the info string
    lines = info_str.split('\n')
    parsed_lines = [line.strip() for line in lines if line.strip()]
    
    # Extract relevant parts
    entries = []
    for line in parsed_lines[5:-2]:  # Skip the non-relevant lines
        parts = line.split()
        col_name = parts[1]
        non_null_count = parts[2]
        dtype = parts[-1]
        entries.append([col_name, non_null_count, dtype])
    
    # Create DataFrame
    info_df = pd.DataFrame(entries, columns=['Column', 'Non-Null Count', 'Dtype'])
    
    return info_df


def count_duplicates(df: pd.DataFrame) -> int:
    """
    Returns the number of duplicate rows in a pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to check for duplicates.

    Returns:
        int: The number of duplicate rows in the DataFrame.
    """
    return df.duplicated().sum()


def generate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a correlation matrix from the numeric columns of a pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to generate the correlation matrix.

    Returns:
        pd.DataFrame: A DataFrame representing the correlation matrix of numeric columns.
    """
    # Select only the numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    return numeric_df.corr()


def generate_data_insights(df: pd.DataFrame, arctic_ops: ArcticOps):

    with st.spinner("Generating data insights ..."):
        if not st.session_state.get("data_insights_output", False):
            prompt = generate_data_insights_prompt(df)
            response = arctic_ops.invoke_snowflake_arctic_simple(prompt)
            response_markdown = ""
            for item in response:
                response_markdown += item
            st.write(response_markdown)
            st.session_state["data_insights_output"] = response_markdown
        else:
            st.markdown(st.session_state["data_insights_output"])
    