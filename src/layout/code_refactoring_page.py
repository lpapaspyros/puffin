import streamlit as st
from typing import Dict
from streamlit_ace import st_ace
import streamlit_antd_components as sac


from utils import ArcticOps


def code_refactoring(refactor_options: Dict) -> None:
    """
    Handles code refactoring, writing new code, or reviewing code based on
    selected functionality.

    Args:
        refactor_options (Dict): Options for code refactoring and generation.
    """

    selected_functionality = get_functionality()
    update_selected_functionality(selected_functionality)

    if selected_functionality in ["Refactor", "Write New Code"]:
        process_code_input(selected_functionality, refactor_options)
    elif selected_functionality == "Review Code":
        st.subheader("Review Code")
        process_review_code_input(refactor_options)


def get_functionality():

    options ={
        "Refactor": "arrow-clockwise", 
        "Write New Code": "plus-circle",
        "Review Code": "search"}
    
    items = [sac.SegmentedItem(
        label = label,
        icon = icon,
    ) for label, icon in options.items()]
    
    selected_functionality = sac.segmented(
        label = "Select Functionality",
        items = items,
        color = "#264C73",
        use_container_width = True,
    )
    return(selected_functionality)


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
        st.session_state["code_refactored"] = False
        st.rerun()


def process_code_input(
    selected_functionality: str, refactor_options: Dict
) -> None:
    """
    Processes user code input based on the selected functionality.

    Args:
        selected_functionality (str): The selected functionality option.
        refactor_options (Dict): Options for code refactoring and generation.
    """
    col1, col2 = st.columns([1, 1 if st.session_state.get("code_refactored", False) else 0.01])
    with col1:
        with st.container(border = True):
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
                st.session_state["code_refactored"] = True
                st.rerun()

    if st.session_state.get("code_refactored", False):
        with col2:
            with st.container(border = True):
                with st.chat_message("assistant"):
                    with st.spinner("Refactoring . . ."):
                        refactored_code = refactor_code(user_input, refactor_options)
                    st.write_stream(refactored_code)
        

def process_review_code_input(refactor_options: Dict) -> None:
    """
    Processes user code input for code review.

    Args:
        refactor_options (Dict): Options for code refactoring and generation.
    """
    user_input = get_user_provided_code(
        refactor_options["refactor_options"]["programming_language"].lower()
    )

    if st.button("Review Code"):
        review_code(user_input, refactor_options)


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
    prompt = generate_prompt(
        user_code_input, refactor_options, functionality="Refactor"
    )
    return(arctic_ops.invoke_snowflake_arctic(prompt))


def review_code(user_code_input: str, refactor_options: Dict) -> None:
    """
    Reviews the user-provided code using ArcticOps.

    Args:
        user_code_input (str): The user-provided code.
        refactor_options (Dict): Options for code refactoring and generation.
    """
    st.session_state["user_code_input"] = user_code_input
    arctic_ops = ArcticOps(
        temperature=refactor_options["model_parameters"]["temperature"],
        top_p=refactor_options["model_parameters"]["top_p"],
    )
    prompt = generate_prompt(
        user_code_input, refactor_options, functionality="Review"
    )
    st.write_stream(arctic_ops.invoke_snowflake_arctic(prompt))


def generate_prompt(
    user_code_input: str, refactor_options: Dict, functionality: str
) -> str:
    """
    Generates a prompt for code refactoring, generation, or review.

    Args:
        user_code_input (str): The user-provided code.
        refactor_options (Dict): Options for code refactoring and generation.
        functionality (str): The selected functionality ("Refactor", "Write New Code", "Review").

    Returns:
        str: The generated prompt.
    """
    refactor_opts = refactor_options["refactor_options"]
    prompt = (
        f"The following {refactor_opts['programming_language']} code is"
        f" provided:\n```\n{user_code_input}\n```\n"
    )
    if functionality == "Refactor":
        prompt += (
            "The code should be refactored and optimized based on the following"
            " criteria:\n"
        )
    elif functionality == "Write New Code":
        prompt += (
            "Based on the requirements, the code should be generated and optimized"
            " based on the following criteria:\n"
        )
    elif functionality == "Review":
        prompt += (
            "Please review the following code with attention to functionality,"
            " readability, efficiency, error handling, security, testing,"
            " adherence to best practices, documentation, and maintainability."
            " Assess whether the code performs as intended and if all features are"
            " correctly implemented. Evaluate the organization and clarity of the"
            " code, including variable names and comments. Check for performance"
            " optimization and identify areas for efficiency improvements. Review"
            " error handling mechanisms and ensure the code gracefully manages"
            " potential errors. Look for security vulnerabilities and verify input"
            " validation and sanitation. Examine the adequacy of testing, ensuring"
            " tests cover all edge cases. Confirm adherence to best practices and"
            " project guidelines, and assess the clarity and completeness of"
            " documentation. Finally, consider the maintainability and scalability"
            " of the code, suggesting any necessary refactoring for better"
            " long-term use. Rate the code in the following categories on a scale"
            " of 1-10: readability, maintainability, performance, and security."
            " Provide a table with the scores and a summary of the review,"
            " including suggestions for improvement."
        )

    if functionality != "Review":
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
                    "- Identify code smells and fix them\n- Suggest remediations"
                    " for code smells and explain why and what should change in"
                    " detail"
                )
            if refactor_opts.get("enable_variable_renaming"):
                criteria.append("- Optimize variable names")
            if refactor_opts.get("suggest_code_organization"):
                criteria.append("- Suggest class and module structure")
            if refactor_opts.get("remove_unused_imports"):
                criteria.append("- Remove unused imports")
            if refactor_opts.get("security_check"):
                criteria.append("- Perform security checks")
        if functionality == "Review":
            criteria.append(
                "- Provide code metrics (e.g., complexity, readability)"
            )
            criteria.append("- Suggest points for improvement")
            criteria.append("- Identify potential bugs or security issues")
            criteria.append("- Evaluate code structure and organization")
        if refactor_opts.get("comment_verbosity"):
            criteria.append(
                f"- Set comment verbosity to {refactor_opts['comment_verbosity']}"
            )
        if refactor_opts.get("programming_language") == "Python":
            criteria.append("- Ensure the code is Pythonic")
        if refactor_opts.get("programming_language") == "SQL":
            criteria.append("- Ensure the code is SQL-compliant")

        prompt += "\n".join(criteria)
        if functionality == "Refactor":
            prompt += (
                "\nProvide the new refactored code and a step-by-step guide on the"
                " changes made."
            )
    return prompt
