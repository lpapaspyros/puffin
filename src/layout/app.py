import streamlit as st
from layout import code_refactoring, data_analysis, homepage, navbar, page_config
from layout.sidebar import sidebar


def init_session_state():
    if "selected_functionality" not in st.session_state:
        st.session_state["selected_functionality"] = None


def run_app():
    page_config()
    page = navbar()
    init_session_state()

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
