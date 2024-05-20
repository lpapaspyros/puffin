import os
import platform
import streamlit as st
from utils.uitls import display_gif, set_page_width

sys = platform.system()
work_dir = (
    os.path.dirname(os.path.abspath(__file__))
    .replace("src\\layout", "")
    .replace("src/layout", "")
)


def homepage():
    set_page_width(900)

    st.markdown(
        """
    # 🐧 Puffin: Your AI Coding Assistant! 🐧

    Welcome to Puffin, your friendly AI-powered coding assistant! Puffin is here to help you refactor, write, and review your code, all powered by the amazing **Snowflake Arctic** language model. Let's dive into what Puffin can do for you!

    ### ✨ Key Features

    1. **Refactor, Write, Review:**
        - **Refactor:** Clean up and optimize your existing code.
        - **Write New Code:** Generate fresh, new code based on your requirements.
        - **Review Code:** Get detailed feedback on your code's functionality, readability, and more!

    2. **User-Friendly Interface:**
        - **Choose Your Task:** Select whether you want to refactor, write new code, or review code with a simple segmented control.
        - **Code Input:** Use our cool ACE editor with syntax highlighting to input your code or requirements.
        - **Real-Time Processing:** Watch Puffin work its magic as it processes your code with the Snowflake Arctic model.

    3. **Meet ArcticOps:**
        - **Your Guide to the Arctic:** ArcticOps is the class that handles all interactions with the Snowflake Arctic model. It keeps track of chat history, ensures prompt limits, and fetches the model's responses.
        - **Smart and Efficient:** From tokenizing prompts to streaming responses, ArcticOps ensures you get the best results from the Snowflake Arctic model.

    4. **Customizable Sidebar:**
        - **Tune Your Settings:** Use the sidebar to tweak model parameters like temperature and top_p, and choose refactoring options tailored to your needs.
        - **Optimize Your Code:** Whether it's ensuring PEP8 compliance or generating docstrings, the sidebar has got you covered.

    ### 🎉 Let's Get Started!

    With Puffin, you can take your coding to the next level. Whether you're cleaning up your code, generating new code, or getting a thorough review, Puffin is here to help. So go ahead, explore the functionalities, and let Puffin make your coding journey smoother and more fun!

    """
    )
    st.divider()

    st.markdown(
        """
    ## :film_projector: Tutorials:

    Welcome to the tutorial for Puffin, your AI-powered coding
    assistant. Follow these steps to learn how to use Puffin's awesome
    features for refactoring, writing, and reviewing code. We'll guide
    you through each functionality with a demo GIF. 
    """
    )

    # Step 1: Choose Your Task
    st.markdown("### 🎨 Step 1: Choose Your Task")
    st.markdown(
        """
    First, decide what you want Puffin to do. You can choose to refactor code, write new code, or review existing code.

    #### Demo - Choosing Your Task:
    """
    )
    gif_path = os.path.join(work_dir, "assets", "gifs", "funct_selection.gif")
    display_gif(gif_path, width="80%")

    # Step 2: Input Your Code or Requirements
    st.markdown("# ")
    st.markdown("### 📝 Step 2: Input Your Code or Requirements")
    st.markdown(
        """
    
    Depending on the task you selected, you'll need to provide some input:
    - **Refactor or Review Code:** Enter your existing code.
    - **Write New Code:** Describe your requirements for the new code.

    Use the ACE editor for a smooth and easy coding experience.

    #### **Demo: Inputting Code/Requirements**
    # """
    )
    gif_path = os.path.join(work_dir, "assets", "gifs", "write_req.gif")
    display_gif(gif_path, width="80%")

    # Step 3: Configure Options
    st.markdown("# ")
    st.markdown("### ⚙️ Step 3: Configure Options")
    st.markdown(
        """
    In the sidebar, you can customize the refactoring options and model
    parameters. Choose your programming language, optimization criteria,
    and other preferences. 

    """
    )

    # Step 4: Process Your Code
    st.markdown("# ")
    st.markdown("### 🚀 Step 4: Process Your Code")
    st.markdown(
        """
    Click the button to let Puffin process your input. Puffin will
    refactor, generate, or review your code using the Snowflake Arctic
    model. 

    #### **Demo: Configuring Options and Generate/Refactor/review  Code**
    # """
    )
    gif_path = os.path.join(work_dir, "assets", "gifs", "generate_code.gif")
    display_gif(gif_path, width="80%")

    # Step 5: View the Results
    st.markdown("# ")
    st.markdown("### 📊 Step 5: View the Results")
    st.markdown(
        """
    Puffin will display the results right in the app. You can see the
    refactored code, newly generated code, or detailed review of your
    code. 
    # """
    )
    # Step 6: Follow-Up Prompts
    st.markdown("# ")
    st.markdown("### 🔄 Step 6: Follow-Up Prompts")
    st.markdown(
        """
    If you have more questions or need further adjustments, use the
    follow-up prompts to continue the conversation with Puffin. 

    #### **Demo: Follow-Up Prompts**
    """
    )
    gif_path = os.path.join(work_dir, "assets", "gifs", "follow_up_prompts.gif")
    display_gif(gif_path, width="80%")

    st.divider()

    st.markdown(
        """
    ## Examples:

    ### Refactor Code

    Let Puffin clean up and optimize your existing code. Just paste your
    code, and Puffin will handle the rest, making it more efficient and
    readable.
    """
    )

    gif_path = os.path.join(work_dir, "assets", "gifs", "example_1.gif")
    display_gif(gif_path, width="80%")

    st.markdown(
        """
    ### Write New Code

    Describe what you need, and Puffin will generate fresh, new code for
    you. It’s like having a personal coder at your fingertips. 
    # """
    )
    gif_path = os.path.join(work_dir, "assets", "gifs", "example_2.gif")
    display_gif(gif_path, width="80%")

    st.markdown(
        """
    ### Review Code

    Get detailed feedback on your code's functionality, readability, and
    more. Puffin reviews your code to ensure it meets the highest
    standards. 

    """
    )
    gif_path = os.path.join(work_dir, "assets", "gifs", "example_3.gif")
    display_gif(gif_path, width="80%")
