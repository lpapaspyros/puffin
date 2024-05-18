import os
import replicate
import streamlit as st
from transformers import AutoTokenizer


class ArcticOps:
    def __init__(self, temperature: float, top_p: float):
        if "REPLICATE_API_TOKEN" in st.secrets:
            replicate_api = st.secrets["REPLICATE_API_TOKEN"]
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
        else:
            raise Exception("Replicate token not found.")

        self.chat_history = []
        self.temperature = temperature
        self.top_p = top_p

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

    def invoke_snowflake_arctic(self, prompt):
        for event in replicate.stream(
            "snowflake/snowflake-arctic-instruct",
            input={
                "prompt": prompt,
                # "prompt_template": r"{prompt}",
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        ):
            yield str(event)
