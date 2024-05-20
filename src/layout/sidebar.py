import json
import streamlit as st
import streamlit_antd_components as sac
from typing import Any, Dict, Tuple


def sidebar(page: str) -> Dict[str, Any]:
    """Generate a sidebar for different pages with specific options.

    Args:
        page: The name of the current page.

    Returns:
        A dictionary containing options based on the provided page.
    """
    side_bar_mods()
    with st.sidebar:
        col1, col2 = st.columns(2)
        col1.image("assets/puffin_logo.png", width=200)
        col2.markdown("# ")
        col2.markdown("# ")
        col2.title("Puffin")

        st.markdown(
            "<h3 style='text-align: center; color: grey;'>Smarter Coding Made"
            " Easy</h3>",
            unsafe_allow_html=True,
        )
        sac.divider(color="black", key="title")

        options = {}
        if page == "CodeLab":
            options = get_code_refactoring_options()
        elif page == "Data Insights":
            options = get_csv_data_analysis_options()

        return options


def side_bar_mods():
    html_injection = """
    <style>
    div[data-testid="stSidebarUserContent"] {
        padding-top: 3rem;
    }
    </style>
    """
    st.markdown(html_injection, unsafe_allow_html=True)

    html_injection = """
    <style>
    .st-emotion-cache-dvne4q {
        padding-right: 1rem;
        padding-bottom: 3rem;
        padding-left: 1rem;
    }
    </style>
    """
    st.markdown(html_injection, unsafe_allow_html=True)


def get_code_refactoring_options() -> Dict[str, Any]:
    """Get options for code refactoring.

    Returns:
        A dictionary containing model parameters and refactor options.
    """
    refactor_options = get_refactor_options()
    temperature, top_p = get_model_parameters()
    sidebar_options = {
        "model_parameters": {"temperature": temperature, "top_p": top_p},
        "refactor_options": refactor_options,
    }
    return sidebar_options


def get_refactor_options() -> Dict[str, Any]:
    """Retrieve and arrange refactoring options based on user selection.

    Returns:
        A dictionary containing refactoring options for the selected language.
    """
    refactor_menu_options = load_refactor_menu_options()
    refactor_options = {}

    with st.expander(":twisted_rightwards_arrows: **Options**", expanded=True):
        programming_language = generate_dropdown(
            "Programming Language",
            refactor_menu_options["programming_languages"],
        )

        optimize_for = generate_multiselect(
            "Optimize for", refactor_menu_options["optimize_for"]
        )

        refactor_options.update(
            {
                "programming_language": programming_language,
                "optimize_for": optimize_for,
            }
        )

        # Additional options for SQL and Python.
        if programming_language == "SQL":
            refactor_options.update(
                {
                    "sql_variant": generate_dropdown(
                        "SQL Variant", refactor_menu_options["sql_variants"]
                    ),
                    "sql_formatting": generate_toggle(
                        "Enforce SQL Formatting", True
                    ),
                }
            )
        elif programming_language == "Python":
            refactor_options["select_pep_compliance"] = generate_multiselect(
                "Select PEP Compliance", refactor_menu_options["pep_list"]
            )

        refactor_options["comment_verbosity"] = generate_dropdown(
            "Comment Verbosity", refactor_menu_options["comment_verbosity"]
        )

        # Docstring and type annotation options for non-SQL languages.
        if programming_language != "SQL":
            docstring_format = st.empty()

            autogenerate_docstring = generate_toggle("Generate docstrings", True)

            if autogenerate_docstring:
                docstring_format = docstring_format.selectbox(
                    "Docstring Format", refactor_menu_options["docstring_formats"]
                )

            refactor_options.update(
                {
                    "autogenerate_docstring": autogenerate_docstring,
                    "include_type_annotations": generate_toggle(
                        "Generate type annotations", True
                    ),
                    "suggest_code_organization": generate_toggle(
                        "Suggest class and module structure", True
                    ),
                }
            )

        # Common options regardless of programming language.
        refactor_options.update(
            {
                "security_check": generate_toggle("Perform security checks", True),
                "identify_code_smells": generate_toggle(
                    "Identify code issues", True
                ),
                "enable_variable_renaming": generate_toggle(
                    "Optimize variable names", True
                ),
            }
        )
        if programming_language != "SQL":
            refactor_options["remove_unused_imports"] = generate_toggle(
                "Remove unused imports", True
            )

        return refactor_options


def generate_toggle(label: str, default: bool) -> bool:
    """Create a toggle switch in the UI.

    Args:
        label: The label for the toggle switch.
        default: The default value for the toggle switch.

    Returns:
        The current state of the toggle switch.
    """
    return st.toggle(label, default)


def generate_dropdown(label: str, options: list) -> Any:
    """Create a dropdown selector in the UI.

    Args:
        label: The label for the dropdown.
        options: The list of options to choose from.

    Returns:
        The currently selected option.
    """
    return st.selectbox(label, options)


def generate_multiselect(label: str, options: list) -> list:
    """Create a multiselect box in the UI.

    Args:
        label: The label for the multiselect box.
        options: The list of options to choose from.

    Returns:
        The list of selected options.
    """
    return st.multiselect(label, options)


def get_model_parameters() -> Tuple[float, float]:
    """Get the model parameters from the user input.

    Returns:
        A tuple containing the temperature and top_p values.
    """
    with st.expander(":hammer_and_wrench: **Model Parameters**", expanded=False):
        temperature = st.slider(
            "Temperature", min_value=0.01, max_value=5.0, value=0.3, step=0.01
        )

        top_p = st.slider(
            "Top P", min_value=0.01, max_value=1.0, value=0.9, step=0.01
        )

    return temperature, top_p


def get_csv_data_analysis_options() -> None:
    """Placeholder function for CSV data analysis options."""
    menu_selection = get_menu_selection()
    temperature, top_p = get_model_parameters()
    if menu_selection == "Data Analysis":
        analysis_options = get_analysis_options()
        sidebar_options = {
            "menu_selection": "Data Analysis",
            "model_parameters": {"temperature": temperature, "top_p": top_p},
            "analysis_options": analysis_options,
        }
    elif menu_selection == "Data Visualizations":
        sidebar_options = {
            "menu_selection": "Data Visualizations",
            "model_parameters": {"temperature": temperature, "top_p": top_p},
            }

    return sidebar_options


def get_menu_selection():

    menu_options = {
        "Data Analysis": "clipboard-data",
        "Data Visualizations": "graph-up"
    }
    menu_items = [sac.MenuItem(label, icon) for label, icon in menu_options.items()]
    with st.expander("Menu", expanded = True):
        menu_selection = sac.menu(
            items = menu_items,
            index = 0,
            variant = "right-bar",
            color = "#264C73"
        )
    return(menu_selection)


def get_analysis_options():

    with st.expander(":mag_right: Options", expanded = True):    
        analysis_options = {}
        analysis_options["data_sample"] = generate_toggle("Display data sample", True)
        analysis_options["descriptive_statistics"] = generate_toggle("Generate descriptive statistics", True)
        analysis_options["data_insights"] = generate_toggle("Generate data insights", True)

    return(analysis_options)


def load_refactor_menu_options() -> Dict[str, Any]:
    """Load refactoring menu options from a JSON file.

    Returns:
        A dictionary of options loaded from the JSON configuration file.
    """
    file_path = "./src/config/refactor_options.json"
    with open(file_path, "r") as refactor_menu_options_json:
        return json.load(refactor_menu_options_json)
