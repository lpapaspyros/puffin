import streamlit as st
from layout import code_refactoring, data_analysis, homepage, navbar, page_config
from layout.sidebar import sidebar
from utils.arctic_operations import ArcticOps


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
    elif page == "CodeLab":
        code_refactoring(options)
    elif page == "Analytics Engine":
        data_analysis()
