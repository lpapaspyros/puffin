import streamlit as st
from streamlit_ace import st_ace

from utils import ArcticOps


def code_refactoring(refactor_options):

    st.subheader("Enter your code here")
    user_code_input = get_user_provided_code(refactor_options["programming_language"].lower())
    refactor_button = st.button("Refactor Code")

    if refactor_button:
        refactor_code(user_code_input, refactor_options)


def get_user_provided_code(language_input):

    user_code_input = st_ace(
        language = language_input,
        theme = "clouds",
        key = "ace_code_input",
        height = 400,
        auto_update = True,
        wrap = True,
        font_size = 13
    )
    return(user_code_input)


def refactor_code(user_code_input, refactor_options):

    st.session_state["user_code_input"] = user_code_input
    arctic_ops = ArcticOps(
        temperature = refactor_options["model_parameters"]["temperature"], 
        top_p = refactor_options["model_parameters"]["temperature"]
        )
    prompt = generate_prompt(user_code_input, refactor_options)
    
    st.write_stream(arctic_ops.invoke_snowflake_arctic(prompt))


def generate_prompt(user_code_input, refactor_options):

    prompt = f"""
    The following code is provided:
    {refactor_options["programming_language"]} 
     
    The code should be refactored and optimized based on the following criteria:\n
    """

    if len(refactor_options["optimize_for"] > 0):
        optimize_for_string = ", ".join(refactor_options["optimize_for"])
        prompt += f"- Optimize code for {optimize_for_string}"
    
    #if refactor_options["optimize_for"]