import streamlit as st
import streamlit_antd_components as sac


def sidebar(page):

    with st.sidebar:

        st.title("Integrated Code Editor and CSV Analysis Platform")
        sac.divider(color = "black", key = "title")