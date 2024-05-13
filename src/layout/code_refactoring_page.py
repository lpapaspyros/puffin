import streamlit as st
from streamlit_ace import st_ace


def code_refactoring():

    st.subheader("Enter your code here")
    user_code_input = get_user_provided_code()
    refactor_button = st.button("Refactor Code")
    if refactor_button:
        pass


def get_user_provided_code():

    user_code_input = st_ace(
        language = "python",
        theme = "clouds",
        key = "ace_code_input",
        height = 400,
        auto_update = True,
        wrap = True,
        font_size = 13
    )
    return(user_code_input)
