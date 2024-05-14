import streamlit as st 

from layout.sidebar import sidebar
from layout import homepage, data_analysis, code_refactoring, page_config, navbar


def run_app():

    page_config()
    page = navbar()
    if page != "Home":
        options = sidebar(page)
    else:
        options = None
    get_page_contents(page, options)


def get_page_contents(page, options):

    if page == "Home":
        homepage()
    elif page == "Code Refactoring":
        code_refactoring(options)
    elif page == "CSV File Data Analysis":
        data_analysis()