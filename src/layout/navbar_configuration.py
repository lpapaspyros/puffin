from streamlit_navigation_bar import st_navbar

def navbar():

    pages = ["Code Refactoring", "CSV File Data Analysis", "GitLab"]
    urls = {"GitLab": "https://gitlab.com/pngts93/arctic-streamlit-hackathon/-/tree/master?ref_type=heads"}

    logo_path = "./assets/Snowflake_Logomark_blue.svg"

    styles = {
        "nav": {
            "background-color": "royalblue",
            "justify-content": "center",
        },
        "img": {
            "padding-right": "14px",
        },
        "span": {
            "color": "white",
            "padding": "14px",
        },
        "active": {
            "background-color": "white",
            "color": "var(--text-color)",
            "font-weight": "normal",
            "padding": "14px",
        }
    }
    options = {
        "show_menu": True,
        "show_sidebar": True,
    }

    page = st_navbar(
        pages,
        logo_path=logo_path,
        urls=urls,
        styles=styles,
        options=options,
    )

    return(page)