import json
import streamlit as st
import streamlit_antd_components as sac


def sidebar(page):
    with st.sidebar:
        col = st.columns(2)
        col[0].image("assets/puffin.png", width=200)
        col[1].markdown("# ")
        col[1].markdown("# ")
        col[1].title("Puffin")

        st.markdown(
            "<h3 style='text-align: center; color: grey;'>AI-Powered Code"
            " Refactoring & Data Insights</h3>",
            unsafe_allow_html=True,
        )
        sac.divider(color="black", key="title")

        if page == "CodeLab":
            options = get_code_refactoring_options()
        if page == "Analytics Engine":
            options = get_csv_data_analysis_options()

        return options


def get_code_refactoring_options():
    refactor_options = get_refactor_options()
    temperature, top_p = get_model_parameters()
    sidebar_options = {
        "model_parameters": {"temperature": temperature, "top_p": top_p},
        "refactor_options": refactor_options,
    }
    return sidebar_options


def get_refactor_options():
    refactor_menu_options = load_refactor_menu_options()
    refactor_options = {}
    refactor = (
        True if st.session_state["selected_functionality"] == "Refactor" else False
    )
    expander_title = (
        ":twisted_rightwards_arrows: **Refactor Options**"
        if refactor
        else ":twisted_rightwards_arrows: **Code Generation Options**"
    )

    with st.expander(expander_title, expanded=True):
        refactor_options["programming_language"] = generate_dropdown(
            label="Programming Language",
            options=refactor_menu_options["programming_languages"],
        )

        refactor_options["optimize_for"] = generate_multiselect(
            label="Optimize for", options=refactor_menu_options["optimize_for"]
        )
        # OPTION FOR SQL
        if refactor_options["programming_language"] == "SQL":
            refactor_options["sql_variant"] = generate_dropdown(
                label="SQL Variant", options=refactor_menu_options["sql_variants"]
            )
            refactor_options["sql_formatting"] = generate_toggle(
                label="Enforce SQL Formatting", default=True
            )
        # OPTION FOR PYTHON
        if refactor_options["programming_language"] == "Python":
            refactor_options["select_pep_compliance"] = generate_multiselect(
                label="Select PEP8 Compliance",
                options=refactor_menu_options["pep_list"],
            )
        # OPTION FOR OTHER LANGUAGES
        if refactor_options["programming_language"] != "SQL":
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

            refactor_options["suggest_code_organization"] = generate_toggle(
                label="Suggest class and module structure", default=True
            )
        # COMMON OPTIONS FOR ALL LANGUAGES
        if refactor:
            refactor_options["security_check"] = generate_toggle(
                label="Perform security checks", default=True
            )
            refactor_options["identify_code_smells"] = generate_toggle(
                label="Identify code issues", default=True
            )

            refactor_options["enable_variable_renaming"] = generate_toggle(
                label="Optimize variable names", default=True
            )
            if refactor_options["programming_language"] != "SQL":
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
