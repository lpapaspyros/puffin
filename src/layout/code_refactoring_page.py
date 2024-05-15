import streamlit as st
from streamlit_ace import st_ace
from typing import Dict
from utils import ArcticOps


def code_refactoring(refactor_options: Dict) -> None:
    """
    Handles code refactoring, writing new code, or reviewing code based on
    selected functionality.

    Args:
        refactor_options (Dict): Options for code refactoring and generation.
    """
    st.subheader("Select Functionality")
    selected_functionality = st.radio(
        "Refactor or Write New Code",
        ["Refactor", "Write New Code", "Review Code"],
        horizontal=True,
        label_visibility="collapsed",
    )

    update_selected_functionality(selected_functionality)

    if selected_functionality in ["Refactor", "Write New Code"]:
        process_code_input(selected_functionality, refactor_options)
    elif selected_functionality == "Review Code":
        st.subheader("Review Code")
        st.write("Code review functionality is not yet implemented.")


def update_selected_functionality(selected_functionality: str) -> None:
    """
    Updates the selected functionality in the session state and triggers a
    rerun if changed.

    Args:
        selected_functionality (str): The selected functionality option.
    """
    if (
        "selected_functionality" not in st.session_state
        or st.session_state["selected_functionality"] != selected_functionality
    ):
        st.session_state["selected_functionality"] = selected_functionality
        st.experimental_rerun()


def process_code_input(
    selected_functionality: str, refactor_options: Dict
) -> None:
    """
    Processes user code input based on the selected functionality.

    Args:
        selected_functionality (str): The selected functionality option.
        refactor_options (Dict): Options for code refactoring and generation.
    """
    st.subheader(
        "Enter your code here"
        if selected_functionality == "Refactor"
        else "Please provide your requirements"
    )
    user_input = (
        get_user_provided_code(
            refactor_options["refactor_options"]["programming_language"].lower()
        )
        if selected_functionality == "Refactor"
        else st.text_area("Enter your requirements here", height=200)
    )
    button_label = (
        "Refactor Code"
        if selected_functionality == "Refactor"
        else "Generate Code"
    )

    if st.button(button_label):
        refactor_code(user_input, refactor_options)


def get_user_provided_code(language_input: str) -> str:
    """
    Gets user-provided code using the ACE editor component.

    Args:
        language_input (str): The programming language for syntax highlighting.

    Returns:
        str: The user-provided code.
    """
    return st_ace(
        language=language_input,
        theme="clouds",
        key="ace_code_input",
        height=400,
        auto_update=True,
        wrap=True,
        font_size=13,
    )


def refactor_code(user_code_input: str, refactor_options: Dict) -> None:
    """
    Refactors the user-provided code using ArcticOps.

    Args:
        user_code_input (str): The user-provided code.
        refactor_options (Dict): Options for code refactoring and generation.
    """
    st.session_state["user_code_input"] = user_code_input
    arctic_ops = ArcticOps(
        temperature=refactor_options["model_parameters"]["temperature"],
        top_p=refactor_options["model_parameters"]["top_p"],
    )
    prompt = generate_prompt(user_code_input, refactor_options)
    st.write_stream(arctic_ops.invoke_snowflake_arctic(prompt))


def generate_prompt(user_code_input: str, refactor_options: Dict) -> str:
    """
    Generates a prompt for code refactoring or generation.

    Args:
        user_code_input (str): The user-provided code.
        refactor_options (Dict): Options for code refactoring and generation.

    Returns:
        str: The generated prompt.
    """
    functionality = st.session_state["selected_functionality"]
    refactor_opts = refactor_options["refactor_options"]
    prompt = (
        f"The following {refactor_opts['programming_language']} code is"
        f" provided:\n```\n{user_code_input}\n```\n"
    )
    prompt += (
        "The code should be refactored and optimized based on the following"
        " criteria:\n"
        if functionality == "Refactor"
        else (
            "Based on the requirements, the code should be generated and optimized"
            " based on the following criteria:\n"
        )
    )

    criteria = []

    if refactor_opts.get("optimize_for"):
        criteria.append(
            f"- Optimize code for {', '.join(refactor_opts['optimize_for'])}"
        )
    if refactor_opts.get("select_pep_compliance"):
        criteria.append(
            "- Ensure PEP compliance for: "
            f"{', '.join(refactor_opts['select_pep_compliance'])}"
        )
    if refactor_opts.get("sql_variant"):
        criteria.append(f"- SQL Variant: {refactor_opts['sql_variant']}")
    if refactor_opts.get("sql_formatting"):
        criteria.append("- Enforce SQL Formatting")
    if refactor_opts.get("autogenerate_docstring"):
        criteria.append("- Autogenerate docstrings")
        if refactor_opts.get("docstring_format"):
            criteria.append(
                f"- Docstring format: {refactor_opts['docstring_format']}"
            )
    if refactor_opts.get("include_type_annotations"):
        criteria.append("- Include type annotations")
    if functionality == "Refactor":
        if refactor_opts.get("identify_code_smells"):
            criteria.append(
                "- Identify code smells and fix them\n- Suggest remediations for"
                " code smells and explain why and what should change in detail"
            )
        if refactor_opts.get("enable_variable_renaming"):
            criteria.append("- Optimize variable names")
        if refactor_opts.get("suggest_code_organization"):
            criteria.append("- Suggest class and module structure")
        if refactor_opts.get("remove_unused_imports"):
            criteria.append("- Remove unused imports")
        if refactor_opts.get("security_check"):
            criteria.append("- Perform security checks")
    if refactor_opts.get("comment_verbosity"):
        criteria.append(
            f"- Set comment verbosity to {refactor_opts['comment_verbosity']}"
        )
    if refactor_opts.get("programming_language") == "Python":
        criteria.append("- Ensure the code is Pythonic")
    if refactor_opts.get("programming_language") == "SQL":
        criteria.append("- Ensure the code is SQL-compliant")

    prompt += "\n".join(criteria)
    prompt += (
        "\nProvide the new refactored code and a step-by-step guide on the changes"
        " made."
    )

    return prompt
