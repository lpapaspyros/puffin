import os
import replicate
import streamlit as st
from streamlit_ace import st_ace
from transformers import AutoTokenizer


def set_page_config():
    """Set the page configuration."""
    st.set_page_config(page_title="Snowflake Arctic Coder Copilot")


def get_icons():
    """Set assistant icon to Snowflake logo."""
    return {"assistant": "./assets/Snowflake_Logomark_blue.svg", "user": "⛷️"}


def sidebar_credentials():
    """Handle Replicate API token input and validation."""
    with st.sidebar:
        st.title("Snowflake Arctic Coder Copilot")
        if "REPLICATE_API_TOKEN" in st.secrets:
            replicate_api = st.secrets["REPLICATE_API_TOKEN"]
        else:
            replicate_api = st.text_input(
                "Enter Replicate API token:", type="password"
            )
            if not (replicate_api.startswith("r8_") and len(replicate_api) == 40):
                st.warning("Please enter your Replicate API token.", icon="⚠️")
                st.markdown(
                    "**Don't have an API token?** Head over to"
                    " [Replicate](https://replicate.com) to sign up for one."
                )
        os.environ["REPLICATE_API_TOKEN"] = replicate_api


def sidebar_refactor_options():
    """Display refactor options in the sidebar."""
    with st.sidebar:
        st.subheader("Refactor Options")
        options = {
            "optimization": st.selectbox(
                "Optimize for:", ["Performance", "Readability", "Memory"]
            ),
            "docstring_format": st.selectbox(
                "Docstring format:", ["Google", "NumPy", "Sphinx"]
            ),
            "type_annotations": st.checkbox("Include type annotations"),
            "pep8_compliance": st.checkbox("Enforce PEP 8 compliance"),
            "line_length": st.slider(
                "Set maximum line length for formatting",
                min_value=50,
                max_value=120,
                value=80,
            ),
            "code_smells": st.checkbox("Detect and suggest fixes for code smells"),
            "variable_renaming": st.checkbox("Enable variable renaming"),
            "class_organization": st.checkbox(
                "Suggest class and module organization"
            ),
            "remove_unused_imports": st.checkbox("Remove unused imports"),
            "generate_docstrings": st.checkbox("Auto-generate docstrings"),
        }
        return options


def initialize_chat():
    """Initialize chat messages."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi. I'm Arctic, a new, efficient, intelligent, and truly open"
                    " language model created by Snowflake AI Research. Ask me"
                    " anything."
                ),
            }
        ]


def display_chat_messages(icons):
    """Display chat messages."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.code(message["content"])


def clear_chat_history():
    """Clear chat history."""
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi. I'm Arctic, a new, efficient, intelligent, and truly open"
                " language model created by Snowflake AI Research. Ask me"
                " anything."
            ),
        }
    ]


def sidebar_clear_history_button():
    """Add a button to clear chat history in the sidebar."""
    st.sidebar.button("Clear chat history", on_click=clear_chat_history)


@st.cache_resource(show_spinner=False)
def get_tokenizer() -> AutoTokenizer:
    """Get a tokenizer to ensure we're not sending too much text to the model."""
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")


def get_num_tokens(prompt: str) -> int:
    """Get the number of tokens in a given prompt."""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)


def user_provided_prompt():
    """Get user-provided code input."""
    return st_ace(
        placeholder="Enter your code here...",
        language="python",
        theme="github",
        key="ace_code_input",
        height=300,
    )


def display_user_input(code_input):
    """Display user input."""
    if code_input:
        st.session_state.messages.append({"role": "user", "content": code_input})
        with st.chat_message("user", avatar="⛷️"):
            st.write(code_input)


def sidebar_model_parameters():
    """Display model parameters in the sidebar."""
    with st.sidebar:
        with st.expander("Model Parameters", expanded=False):
            st.subheader("Adjust model parameters")
            temperature = st.slider(
                "Temperature", min_value=0.01, max_value=5.0, value=0.3, step=0.01
            )
            top_p = st.slider(
                "Top P", min_value=0.01, max_value=1.0, value=0.9, step=0.01
            )
            return temperature, top_p


def generate_arctic_response(options, temperature, top_p):
    """Generate a response from the Snowflake Arctic model."""
    prompt = []
    for dict_message in st.session_state.messages:
        role = dict_message["role"]
        content = dict_message["content"]
        prompt.append(f"{role}\n{content}\n")

    # Adding refactoring options to the prompt
    refactor_options = (
        "Refactor the code considering the following options:\n"
        f"Optimize for: {options['optimization']}\n"
        f"Docstring format: {options['docstring_format']}\n"
        f"Type annotations: {options['type_annotations']}\n"
        f"PEP 8 compliance: {options['pep8_compliance']}\n"
        f"Maximum line length for formatting: {options['line_length']}\n"
        f"Detect code smells: {options['code_smells']}\n"
        f"Enable variable renaming: {options['variable_renaming']}\n"
        f"Suggest class and module organization: {options['class_organization']}\n"
        f"Remove unused imports: {options['remove_unused_imports']}\n"
        f"Generate docstrings: {options['generate_docstrings']}\n"
    )

    prompt.append(f"assistant\n{refactor_options}")
    prompt_str = "\n".join(prompt)

    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        st.button(
            "Clear chat history",
            on_click=clear_chat_history,
            key="clear_chat_history",
        )
        st.stop()

    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input={
            "prompt": prompt_str,
            "prompt_template": r"{prompt}",
            "temperature": temperature,
            "top_p": top_p,
        },
    ):
        yield str(event)


def generate_response_if_needed(options, temperature, top_p):
    """Generate a response if the last message is not from the assistant."""
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="./assets/Snowflake_Logomark_blue.svg"):
            response = generate_arctic_response(options, temperature, top_p)
            full_response = st.write_stream(response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)


def main():
    """Main function to run the app."""
    set_page_config()
    icons = get_icons()
    sidebar_credentials()
    options = sidebar_refactor_options()
    initialize_chat()
    display_chat_messages(icons)
    sidebar_clear_history_button()
    code_input = user_provided_prompt()
    display_user_input(code_input)
    temperature, top_p = sidebar_model_parameters()
    generate_response_if_needed(options, temperature, top_p)


if __name__ == "__main__":
    main()
