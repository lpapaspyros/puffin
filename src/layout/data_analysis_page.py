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
        if uploaded_file:
            load_dataset_button = st.button("Load Dataset")
            if load_dataset_button:
                df = load_data_to_dataframe(uploaded_file)
                st.session_state["dataframe"] = df

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
    
    if st.session_state.get("visualization_insights"):
        with st.container(border = True):
            st.subheader("Visualization Insights")
            st.write_stream(st.session_state["visualization_insights"])
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
    You are an expert in data and statistical analysis and finding meaningfull insights from data. You have been 
    provided with a data set in the form of a dataframe. You will be given the column names of the dataframe, the 
    dtypes of the dataframe, a random sample of the dataframe, and the descriptive statistics of a dataframe. 
    With these information try to identify and isolate key characteristics of the data set and provide useful
    insights and propose more ways to further analyze the data.

    -Dataframe Columns:
    {df.columns} 

    -Dataframe Columns Dtypes:
    {df.dtypes}

    -Dataframe Data Sample:
    {get_random_sample(df)}

    -Dataframe Descriptive Statistics:
    {df.describe()}
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
        if analysis_options["descriptive_statistics"]:
            with st.expander("**Descriptive Statistics**", expanded = True):
                st.write(generate_descriptive_statistics(df))
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


def generate_data_insights(df: pd.DataFrame, arctic_ops: ArcticOps):

    prompt = generate_data_insights_prompt(df)
    response = arctic_ops.invoke_snowflake_arctic_simple(prompt)
    st.write_stream(response)