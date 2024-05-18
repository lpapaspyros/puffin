import os
import replicate
import streamlit as st
from transformers import AutoTokenizer


class ArcticOps:
    def __init__(
        self, temperature: float, top_p: float, init_chat_history: bool = True
    ):
        if "REPLICATE_API_TOKEN" in st.secrets:
            replicate_api = st.secrets["REPLICATE_API_TOKEN"]
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
        else:
            raise Exception("Replicate token not found.")

        self.chat_history = []
        self.temperature = temperature
        self.top_p = top_p
        st.session_state.chat_aborted = False
        st.session_state.unique_id_counter = 0
        if init_chat_history:
            self.init_chat_history()

    @staticmethod
    def init_chat_history():
        """Create a st.session_state.messages list to store chat messages"""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hi. I'm Puffin how i can help you today?",
                }
            ]

    @staticmethod
    def abort_chat(error_message: str):
        """Display an error message requiring the chat to be cleared.
        Forces a rerun of the app."""
        assert error_message, "Error message must be provided."
        error_message = f":red[{error_message}]"
        if st.session_state.messages[-1]["role"] != "assistant":
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )
        else:
            st.session_state.messages[-1]["content"] = error_message
        st.session_state.chat_aborted = True
        st.rerun()

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def get_tokenizer(model_name: str = "huggyllama/llama-7b") -> AutoTokenizer:
        """Get a tokenizer to ensure we're not sending too much text to the model."""
        return AutoTokenizer.from_pretrained(model_name)

    def get_num_tokens(self, prompt: str) -> int:
        """Get the number of tokens in a given prompt."""
        tokenizer = self.get_tokenizer()
        tokens = tokenizer.tokenize(prompt)
        return len(tokens)

    def check_num_tokens_limit(self, num_tokens):
        if num_tokens >= 3072:
            st.stop()

    def invoke_snowflake_arctic(self):
        prompt_list = []
        for dict_message in st.session_state.messages:
            if dict_message["role"] == "user":
                prompt_list.append(
                    {"role": "user", "content": dict_message["content"]}
                )
            else:
                prompt_list.append(
                    {"role": "assistant", "content": dict_message["content"]}
                )

        prompt_str = ""
        for message in prompt_list:
            prompt_str += f"{message['role']}\n{message['content']}\n"

        num_tokens = self.get_num_tokens(prompt_str)
        max_tokens = 1500

        if num_tokens >= max_tokens:
            self.abort_chat(
                "Conversation length too long. Please keep it under"
                f" {max_tokens} tokens."
            )

        for event in replicate.stream(
            "snowflake/snowflake-arctic-instruct",
            input={
                "prompt": prompt_str,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        ):
            yield str(event)

    def send_prompt(self, prompt):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            response = self.invoke_snowflake_arctic()
            with st.container(border=True):
                st.write_stream(response)
            # self.get_and_process_prompt()

    def get_and_process_prompt(self):
        """Get the user prompt and process it"""
        col = st.columns([2, 2, 1.8, 10, 1, 2], gap="small")
        create_space_markdown = "<p style='font-size:9px;'> .</p>"

        st.session_state.unique_id_counter += 1
        unique_id = st.session_state.unique_id_counter

        col[1].markdown(create_space_markdown, unsafe_allow_html=True)
        if col[1].button(
            ":test_tube: Create Unit Test",
            key=f"create_unit_test_{unique_id}",
            use_container_width=True,
        ):
            prompt = "Create Unit Test"
            self.send_prompt(prompt)

        col[2].markdown(create_space_markdown, unsafe_allow_html=True)
        if col[2].button(
            ":hammer_and_pick: How to use",
            key=f"how_to_use_{unique_id}",
            use_container_width=True,
        ):
            prompt = (
                "Show me step by step and with examples how to use the provided"
                " code and how to implement it"
            )
            self.send_prompt(prompt)

        prompt = col[3].text_input(
            "Enter your follow up message:",
            key=f"user_input_{unique_id}",
        )

        col[4].markdown(create_space_markdown, unsafe_allow_html=True)
        if col[4].button("Send", key=f"send_message_{unique_id}"):
            self.send_prompt(prompt)
