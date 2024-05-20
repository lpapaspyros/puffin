import base64
import streamlit as st


def display_gif(gif_path, width=None, height=None):
    """
    Display a GIF from a local file in a Streamlit app.

    Parameters:
    gif_path (str): Path to the GIF file to be displayed.
    width (str, optional): Width of the GIF (e.g., '500px', '50%'). Defaults to None.
    height (str, optional): Height of the GIF (e.g., '500px', '50%'). Defaults to None.
    """
    # Open the GIF file in binary mode
    with open(gif_path, "rb") as file_:
        contents = file_.read()

    # Encode the GIF file to base64
    data_url = base64.b64encode(contents).decode("utf-8")

    # Create the img tag with optional width and height
    img_tag = f'<img src="data:image/gif;base64,{data_url}" alt="GIF"'
    if width:
        img_tag += f' width="{width}"'
    if height:
        img_tag += f' height="{height}"'
    img_tag += ">"

    # Display the GIF using HTML
    st.markdown(img_tag, unsafe_allow_html=True)


def set_page_width(width: int):
    """Set the page width for a Streamlit app with custom CSS.

    Args:
        width (int): The maximum width in pixels for the content area.
    """
    style = f"""
    <style>
    .main .block-container {{
        max-width: {width}px;
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
