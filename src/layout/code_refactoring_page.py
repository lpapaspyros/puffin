import streamlit as st
import streamlit_antd_components as sac
from streamlit_ace import st_ace
from typing import Dict
from utils import ArcticOps


def code_refactoring(refactor_options: Dict) -> ArcticOps:
    """
    Handles code refactoring, writing new code, or reviewing code based on
    selected functionality.

    Args:
        refactor_options (Dict): Options for code refactoring and generation.

    Returns:
        ArcticOps: The ArcticOps object used for code processing.
    """
    selected_functionality = get_functionality()
    update_selected_functionality(selected_functionality)

    process_code(selected_functionality, refactor_options)
    if st.session_state.get("code_refactored", False):
        handle_follow_up_prompt(refactor_options)
    return


@st.experimental_fragment
def handle_follow_up_prompt(refactor_options):
    arctic_ops = ArcticOps(
        temperature=refactor_options["model_parameters"]["temperature"],
        top_p=refactor_options["model_parameters"]["top_p"],
        init_chat_history=False,
    )
    arctic_ops.get_and_process_prompt()
    # st.json(st.session_state.messages) # Uncomment to see the messages in JSON format


def get_functionality():
    options = {
        "Refactor": "arrow-clockwise",
        "Write New Code": "plus-circle",
        "Review Code": "search",
    }

    items = [
        sac.SegmentedItem(
            label=label,
            icon=icon,
        )
        for label, icon in options.items()
    ]

    selected_functionality = sac.segmented(
        label="Select Functionality",
        items=items,
        color="#264C73",
        use_container_width=True,
    )
    return selected_functionality


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


def process_code(selected_functionality: str, refactor_options: Dict) -> ArcticOps:
    """
    Processes user code input based on the selected functionality.

    Args:
        selected_functionality (str): The selected functionality option.
        refactor_options (Dict): Options for code refactoring and generation.

    Returns:
        ArcticOps: The ArcticOps object used for code processing.
    """
    col1, col2 = st.columns(
        [1, 1 if st.session_state.get("code_refactored", False) else 0.01]
    )
    with col1:
        with st.container(border=True):
            if selected_functionality == "Review Code":
                st.subheader("Review Code")
            else:
                st.subheader(
                    "Enter your code here"
                    if selected_functionality == "Refactor"
                    else "Please provide your requirements"
                )

            user_input = (
                get_user_provided_code(
                    refactor_options["refactor_options"][
                        "programming_language"
                    ].lower()
                )
                if selected_functionality in ["Refactor", "Review Code"]
                else st.text_area("Enter your requirements here", height=200)
            )

            button_label = {
                "Refactor": "Refactor Code",
                "Write New Code": "Generate Code",
                "Review Code": "Review Code",
            }[selected_functionality]

            if st.button(button_label):
                st.session_state["code_refactored"] = True
                st.session_state["user_input"] = user_input
                st.session_state["messages"] = []
                st.rerun()

    if st.session_state.get("code_refactored", False):
        with col2:
            with st.container(border=True):
                with st.chat_message("assistant"):
                    with st.spinner("Processing . . ."):
                        arctic_ops = ArcticOps(
                            temperature=refactor_options["model_parameters"][
                                "temperature"
                            ],
                            top_p=refactor_options["model_parameters"]["top_p"],
                        )

                        result = refactor_code(
                            user_input, arctic_ops, refactor_options
                        )
                        st.write_stream(result)
                        return arctic_ops


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


def refactor_code(
    user_input: str, arctic_ops: ArcticOps, refactor_options: Dict
) -> str:
    """
    Refactors or Review the user-provided code using ArcticOps.

    Args:
        user_input (str): The user-provided code.
        arctic_ops (ArcticOps): The ArcticOps object.
        refactor_options (Dict): Options for code refactoring and generation.

    Returns:
        str: The refactored code.
    """
    generate_prompt(user_input, refactor_options)
    return arctic_ops.invoke_snowflake_arctic()


def generate_prompt(user_input: str, refactor_options: Dict) -> str:
    """
    Generates a prompt for code refactoring, generation, or review.

    Args:
        user_input (str): The user-provided code.
        refactor_options (Dict): Options for code refactoring and generation.

    Returns:
        str: The generated prompt.
    """
    refactor_opts = refactor_options["refactor_options"]
    functionality = st.session_state["selected_functionality"]
    if functionality in ["Review Code", "Refactor"]:
        prompt = (
            f"The following {refactor_opts['programming_language']} code is"
            f" provided:\n```\n{user_input}\n```\n"
        )
    elif functionality == "Write New Code":
        prompt = (
            "I want you to write a new code in"
            f" {refactor_opts['programming_language']} that fulfills the following"
            f" requirements:\n {user_input}\n"
        )
        prompt += (
            "Based on the requirements, the code should be generated and optimized"
            " based on the following criteria:\n"
        )
    if functionality == "Review Code":
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
            " including suggestions for improvement.\n Return your score in a"
            " table html format "
        )

    if functionality == "Refactor":
        prompt += (
            "The code should be refactored and optimized based on the following"
            " criteria:\n"
        )

    if functionality != "Review Code":
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
        if functionality == "Review Code":
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
    # add prompt to session stat
    st.session_state.messages.append({"role": "user", "content": prompt})
    return prompt


if __name__ == "__main__":
    pass
