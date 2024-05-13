import streamlit as st 

from layout.sidebar import sidebar
from layout import homepage, data_analysis, code_refactoring
from config import page_config, navbar


def run_app():

    page_config()
    page = navbar()
    options = sidebar(page)
    get_page_contents(page, options)


def get_page_contents(page, options):

    if page == "Home":
        homepage()
    elif page == "Code Refactoring":
        code_refactoring()
    elif page == "CSV File Data Analysis":
        data_analysis()