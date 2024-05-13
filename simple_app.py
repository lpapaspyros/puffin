import os
import replicate
import streamlit as st
from streamlit_ace import st_ace
from transformers import AutoTokenizer

# Set assistant icon to Snowflake logo
icons = {"assistant": "./Snowflake_Logomark_blue.svg", "user": "⛷️"}

# App title
st.set_page_config(page_title="Snowflake Arctic Coder Copilot")

# Replicate Credentials
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
    st.subheader("Adjust model parameters")
    temperature = st.sidebar.slider(
        "temperature", min_value=0.01, max_value=5.0, value=0.3, step=0.01
    )
    top_p = st.sidebar.slider(
        "top_p", min_value=0.01, max_value=1.0, value=0.9, step=0.01
    )

# Additional options
with st.sidebar:
    st.subheader("Refactor Options")
    optimization = st.selectbox(
        "Optimize for:", ["Performance", "Readability", "Memory"]
    )
    docstring_format = st.selectbox(
        "Docstring format:", ["Google", "NumPy", "Sphinx"]
    )
    type_annotations = st.checkbox("Include type annotations")
    pep8_compliance = st.checkbox("Enforce PEP 8 compliance")

# Store LLM-generated responses
if "messages" not in st.session_state.keys():
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

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])


def clear_chat_history():
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


st.sidebar.button("Clear chat history", on_click=clear_chat_history)


@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text to the Model. Eventually we will replace this with ArcticTokenizer"""
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")


def get_num_tokens(prompt):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)


# Function for generating Snowflake Arctic response
def generate_arctic_response():
    prompt = []
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            prompt.append("user\n" + dict_message["content"] + "")
        else:
            prompt.append("assistant\n" + dict_message["content"] + "")

    # Adding refactoring options to the prompt
    prompt.append("assistant")
    prompt.append(
        "Refactor the code considering the following options:\n"
        f"Optimize for: {optimization}\n"
        f"Docstring format: {docstring_format}\n"
        f"Type annotations: {type_annotations}\n"
        f"PEP 8 compliance: {pep8_compliance}\n"
    )
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


# User-provided prompt
code_input = st_ace(
    placeholder="Enter your code here...",
    language="python",
    theme="github",
    key="ace_code_input",
    height=300,
)

if code_input:
    st.session_state.messages.append({"role": "user", "content": code_input})
    with st.chat_message("user", avatar="⛷️"):
        st.write(code_input)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar="./Snowflake_Logomark_blue.svg"):
        response = generate_arctic_response()
        full_response = st.write_stream(response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
