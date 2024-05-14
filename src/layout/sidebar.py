import json
import streamlit as st
import streamlit_antd_components as sac


def sidebar(page):
    with st.sidebar:
        st.markdown(
            "<h1 style='text-align: center; color: black;'>CodeGenie</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: grey;'>AI-Powered Code"
            " Refactoring & Data Insights</h3>",
            unsafe_allow_html=True,
        )
        sac.divider(color="black", key="title")

        if page == "Code Refactoring":
            options = get_code_refactoring_options()
        elif page == "CSV File Data Analysis":
            options = get_csv_data_analysis_options()

        return options


def get_code_refactoring_options():
    temperature, top_p = get_model_parameters()
    refactor_options = get_refactor_options()
    sidebar_options = {
        "model_parameters": {"temperature": temperature, "top_p": top_p},
        "refactor_options": refactor_options,
    }
    return sidebar_options


def get_refactor_options():
    refactor_menu_options = load_refactor_menu_options()
    refactor_options = {}

    with st.expander(
        ":twisted_rightwards_arrows: **Refactor Options**", expanded=True
    ):
        refactor_options["programming_language"] = generate_dropdown(
            label="Programming Language",
            options=refactor_menu_options["programming_languages"],
        )

        if refactor_options["programming_language"] == "SQL":
            refactor_options["sql_variant"] = generate_dropdown(
                label="SQL Variant", options=refactor_menu_options["sql_variants"]
            )

        refactor_options["optimize_for"] = generate_multiselect(
            label="Optimize for", options=refactor_menu_options["optimize_for"]
        )
        refactor_options["select_pep_compliance"] = generate_multiselect(
            label="Select PEP8 Compliance",
            options=refactor_menu_options["pep_list"],
        )

        docstring_format = st.empty()

        refactor_options["autogenerate_docstring"] = generate_toggle(
            label="Generate docstrings", default=True
        )

        if refactor_options["autogenerate_docstring"]:
            docstring_format = docstring_format.selectbox(
                label="Docstring Format",
                options=refactor_menu_options["docstring_formats"],
            )

        refactor_options["include_type_annotations"] = generate_toggle(
            label="Generate type annotations", default=True
        )

        refactor_options["identify_code_smells"] = generate_toggle(
            label="Identify code smells", default=True
        )

        if refactor_options["identify_code_smells"]:
            refactor_options["suggest_fixes"] = generate_toggle(
                label="Suggest remediations for code anomalies", default=True
            )

        refactor_options["enable_variable_renaming"] = generate_toggle(
            label="Optimize variable names", default=True
        )

        refactor_options["suggest_code_organization"] = generate_toggle(
            label="Suggest class and module structure", default=True
        )

        refactor_options["remove_unused_imports"] = generate_toggle(
            label="Remove unused imports", default=True
        )
        refactor_options["comment_verbosity"] = generate_dropdown(
            label="Comment Verbosity",
            options=refactor_menu_options["comment_verbosity"],
        )
        return refactor_options


def generate_toggle(label, default):
    selection = st.toggle(label=label, value=default)
    return selection


def generate_dropdown(label, options):
    selection = st.selectbox(label=label, options=options)
    return selection


def generate_multiselect(label, options):
    selections = st.multiselect(label=label, options=options)
    return selections


def get_model_parameters():
    with st.expander(":hammer_and_wrench: **Model Parameters**", expanded=False):
        temperature = st.slider(
            label="Temperature",
            min_value=0.01,
            max_value=5.0,
            value=0.3,
            step=0.01,
        )

        top_p = st.slider(
            label="Top P", min_value=0.01, max_value=1.0, value=0.9, step=0.01
        )

    return (temperature, top_p)


def get_csv_data_analysis_options():
    pass


def load_refactor_menu_options():
    file_path = "./src/config/refactor_options.json"
    with open(file_path, "r") as refactor_menu_options_json:
        refactor_menu_options = json.load(refactor_menu_options_json)
    return refactor_menu_options
