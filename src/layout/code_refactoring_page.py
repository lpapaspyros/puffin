import streamlit as st
from streamlit_ace import st_ace
from utils import ArcticOps


def code_refactoring(refactor_options):
    st.subheader("Select Functionality")
    selected_functionality = st.radio(
        "Refactor or Write New Code",
        ["Refactor", "Write New Code", " Review Code"],
        horizontal=True,
        label_visibility="collapsed",
    )

    update_selected_functionality(selected_functionality)

    if selected_functionality == "Refactor":
        st.subheader("Enter your code here")
        user_input = get_user_provided_code(
            refactor_options["refactor_options"]["programming_language"].lower()
        )
        refactor_button = st.button("Refactor Code")

        if refactor_button:
            refactor_code(user_input, refactor_options)
    elif selected_functionality == "Write New Code":
        st.subheader("Please provide your requirements")
        user_input = st.text_area("Enter your requirements here", height=200)
        refactor_button = st.button("Generate Code")

        if refactor_button:
            refactor_code(user_input, refactor_options)
    elif selected_functionality == " Review Code":
        st.subheader("Review Code")
        st.write("Code review functionality is not yet implemented.")


def update_selected_functionality(selected_functionality):
    if "selected_functionality" not in st.session_state:
        st.session_state["selected_functionality"] = selected_functionality
    elif st.session_state["selected_functionality"] != selected_functionality:
        st.session_state["selected_functionality"] = selected_functionality
        st.rerun()


def get_user_provided_code(language_input):
    user_code_input = st_ace(
        language=language_input,
        theme="clouds",
        key="ace_code_input",
        height=400,
        auto_update=True,
        wrap=True,
        font_size=13,
    )
    return user_code_input


def refactor_code(user_code_input, refactor_options):
    st.session_state["user_code_input"] = user_code_input
    arctic_ops = ArcticOps(
        temperature=refactor_options["model_parameters"]["temperature"],
        top_p=refactor_options["model_parameters"]["temperature"],
    )
    prompt = generate_prompt(user_code_input, refactor_options["refactor_options"])

    st.write_stream(arctic_ops.invoke_snowflake_arctic(prompt))


def generate_prompt(user_code_input, refactor_options):
    refactor = (
        True if st.session_state["selected_functionality"] == "Refactor" else False
    )
    if refactor:
        prompt = f"""
        The following {refactor_options["programming_language"]} code is provided:
        ```
        {user_code_input}
        ```
        The code should be refactored and optimized based on the following criteria:\n
        """
    elif st.session_state["selected_functionality"] == "Write New Code":
        prompt = f"""
        The following requirements are provided:
        ```
        {user_code_input}
        ```
        Based on the requirements, the code should be generated and optimized based on the following criteria:\n
        """

    if len(refactor_options["optimize_for"]) > 0:
        optimize_for_string = ", ".join(refactor_options["optimize_for"])
        prompt += f"- Optimize code for {optimize_for_string}\n"

    if (
        "select_pep_compliance" in refactor_options
        and len(refactor_options["select_pep_compliance"]) > 0
    ):
        pep_compliance_string = ", ".join(
            refactor_options["select_pep_compliance"]
        )
        prompt += f"- Ensure PEP compliance for: {pep_compliance_string}\n"
    if refactor_options.get("sql_variant"):
        prompt += f"- SQL Variant: {refactor_options['sql_variant']}\n"
    if refactor_options.get("sql_formatting"):
        prompt += "- Enforce SQL Formatting\n"

    if refactor_options.get("autogenerate_docstring"):
        prompt += "- Autogenerate docstrings\n"
        if refactor_options.get("docstring_format"):
            prompt += (
                f"- Docstring format: {refactor_options['docstring_format']}\n"
            )
    if refactor_options.get("include_type_annotations"):
        prompt += "- Include type annotations\n"
    if refactor and refactor_options.get("identify_code_smells"):
        prompt += (
            "- Identify code smells and fix them\n"
            "- Suggest remediations for code smells and explain why and what"
            " should change in detail\n"
        )
    if refactor and refactor_options.get("enable_variable_renaming"):
        prompt += "- Optimize variable names\n"
    if refactor and refactor_options.get("suggest_code_organization"):
        prompt += "- Suggest class and module structure\n"
    if refactor and refactor_options.get("remove_unused_imports"):
        prompt += "- Remove unused imports\n"
    if refactor and refactor_options.get("security_check"):
        prompt += "- Perform security checks\n"
    if refactor_options.get("comment_verbosity"):
        prompt += (
            f"- Set comment verbosity to {refactor_options['comment_verbosity']}\n"
        )
    if refactor_options.get("programming_language") == "Python":
        prompt += "- Ensure the code is Pythonic\n"
    if refactor_options.get("programming_language") == "SQL":
        prompt += "- Ensure the code is SQL-compliant\n"

    prompt += (
        "\nProvide the new refactored code and a step-by-step guide on the changes"
        " made."
    )
    return prompt
