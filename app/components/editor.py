import streamlit as st

def editor_component(text:str):
    return st.text_area(
        "Edit Meeting Minutes (optional):",
        value=text,
        height=400
    )
