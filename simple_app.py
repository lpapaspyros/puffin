import os
import streamlit as st
from streamlit_ace import st_ace
from transformers import AutoTokenizer

# Define constants for API token validation and message initialization
API_TOKEN_PREFIX = "r8_"
API_TOKEN_LENGTH = 40
TOKEN_LIMIT = 3072
DEFAULT_ASSISTANT_MESSAGE = (
    "Hi. I'm Arctic, a new, efficient, intelligent, and truly open "
    "language model created by Snowflake AI Research. Ask me anything."
)


def set_page_config() -> None:
    """Set Streamlit page configuration."""
    st.set_page_config(page_title="Snowflake Arctic Coder Copilot")


def load_icons() -> dict:
    """Load icons for chat roles.

    Returns:
        dict: A dictionary mapping roles to their respective icons.
    """
    return {"assistant": "./Snowflake_Logomark_blue.svg", "user": "⛷️"}


def retrieve_api_token() -> str:
    """Retrieve and validate the Replicate API token provided by the user.

    Returns:
        str: A valid Replicate API token.
    """
    with st.sidebar:
        st.title("Snowflake Arctic Coder Copilot")

        replicate_api = st.secrets.get("REPLICATE_API_TOKEN")
        if not replicate_api:
            replicate_api = st.text_input(
                "Enter Replicate API token:", type="password"
            )
            if not (
                replicate_api.startswith(API_TOKEN_PREFIX)
                and len(replicate_api) == API_TOKEN_LENGTH
            ):
                st.warning("Please enter your Replicate API token.", icon="⚠️")
                st.markdown(
                    "**Don't have an API token?** Head over to "
                    "[Replicate](https://replicate.com) to sign up for one."
                )
        os.environ["REPLICATE_API_TOKEN"] = replicate_api
    return replicate_api


def configure_sidebar(language: str) -> dict:
    """Configure sidebar options for code refactoring.

    Args:
        language (str): Selected programming language.

    Returns:
        dict: A dictionary containing the selected refactor options.
    """
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
                "Set maximum line length for formatting", 50, 120, 80
            ),
            "code_smells": st.checkbox("Detect and suggest fixes for code smells"),
            "variable_renaming": st.checkbox("Enable variable renaming"),
            "class_organization": st.checkbox(
                "Suggest class and module organization"
            ),
            "remove_unused_imports": st.checkbox("Remove unused imports"),
            "generate_docstrings": st.checkbox("Auto-generate docstrings"),
        }
        if language == "SQL":
            options["sql_optimization"] = st.checkbox("Optimize SQL queries")
        return options


def initialize_chat() -> None:
    """Initialize chat messages in session state."""
    st.session_state.setdefault(
        "messages",
        [
            {
                "role": "assistant",
                "content": DEFAULT_ASSISTANT_MESSAGE,
            }
        ],
    )


def display_chat_messages(icons: dict, language: str) -> None:
    """Display chat history on the main page.

    Args:
        icons (dict): Dictionary of icons for each role.
        language (str): Selected programming language.
    """
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.code(message["content"], language=language)


def clear_chat_history() -> None:
    """Clear the chat history."""
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": DEFAULT_ASSISTANT_MESSAGE,
        }
    ]


def add_sidebar_clear_button() -> None:
    """Add a button to clear chat history in the sidebar."""
    st.sidebar.button("Clear chat history", on_click=clear_chat_history)


@st.cache_resource(show_spinner=False)
def get_tokenizer() -> AutoTokenizer:
    """Fetch or initialize the tokenizer.

    Returns:
        AutoTokenizer: The tokenizer instance.
    """
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")


def count_tokens(prompt: str) -> int:
    """Count the number of tokens for the given prompt using the tokenizer.

    Args:
        prompt (str): Text to be tokenized.

    Returns:
        int: The number of tokens.
    """
    return len(get_tokenizer().tokenize(prompt))


def get_user_code(language: str) -> str:
    """Prompt the user to enter code and return it.

    Args:
        language (str): Selected programming language.

    Returns:
        str: User-provided code.
    """
    return st_ace(
        placeholder=f"Enter your {language} code here...",
        language=language,
        theme="github",
        key="ace_code_input",
        height=300,
    )


def append_user_code(user_code: str) -> None:
    """Append user's code input to the chat history.

    Args:
        user_code (str): Code provided by the user.
    """
    if user_code:
        st.session_state["messages"].append({"role": "user", "content": user_code})
        with st.chat_message("user", avatar=load_icons()["user"]):
            st.write(user_code)


def refine_model_parameters() -> tuple:
    """Allow users to adjust model parameters via the sidebar.

    Returns:
        tuple: A tuple containing the temperature and top_p settings.
    """
    with st.sidebar:
        with st.expander("Model Parameters", expanded=False):
            temperature = st.slider(
                "Temperature", min_value=0.01, max_value=5.0, value=0.3, step=0.01
            )
            top_p = st.slider(
                "Top P", min_value=0.01, max_value=1.0, value=0.9, step=0.01
            )
    return temperature, top_p


def generate_arctic_response(
    options: dict, temperature: float, top_p: float
) -> str:
    """Generate a response from the Snowflake Arctic model based on user inputs and options.

    Args:
        options (dict): Refactoring options chosen by the user.
        temperature (float): Model temperature setting.
        top_p (float): Model top_p setting.

    Returns:
        str: The generated response text.
    """
    prompt = [f"{m['role']}\n{m['content']}" for m in st.session_state["messages"]]
    options_str = "\n".join(f"{k}: {v}" for k, v in options.items())
    prompt.append(
        "assistant\nRefactor the code considering the following"
        f" options:\n{options_str}"
    )

    prompt_text = "\n".join(prompt)

    if count_tokens(prompt_text) > TOKEN_LIMIT:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        clear_chat_history()
        st.button(
            "Clear chat history",
            on_click=clear_chat_history,
            key="btn_clear_history",
        )
        return ""

    # You need to replace this part with actual model generation logic
    generated_response = "<Placeholder for the model response>"

    return generated_response


def main() -> None:
    """Run the main application flow."""
    set_page_config()
    icons = load_icons()
    api_token = retrieve_api_token()
    if not api_token:
        return  # Exit if no valid token is provided

    language = st.sidebar.selectbox("Select Language", ["python", "sql"])

    refactor_options = configure_sidebar(language)
    initialize_chat()
    display_chat_messages(icons, language)
    user_code = get_user_code(language)
    append_user_code(user_code)
    temperature, top_p = refine_model_parameters()

    if "generate" in st.session_state and st.session_state["generate"]:
        response = generate_arctic_response(refactor_options, temperature, top_p)
        if response:
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            with st.chat_message("assistant", avatar=icons["assistant"]):
                st.code(response, language=language)

    if st.button("Generate"):
        st.session_state["generate"] = True
    else:
        st.session_state["generate"] = False
    add_sidebar_clear_button()


if __name__ == "__main__":
    main()
