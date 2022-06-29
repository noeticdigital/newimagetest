import streamlit as st
from htbuilder import svg, ellipse

def render():
    data = ['', '']
    col1, col2 = st.columns(2)

    with col1:
        emoji = st.text_input('Emoji', placeholder='🚢', help="If you leave it empty, we'll default it to :rocket:")
        if emoji is not '': data[0] = emoji

    with col2:
        version_number = st.text_input('Version number', placeholder='v.1.10.0', help="This text shows up at the bottom-right hand-corner")
        if version_number is not '': data[1] = version_number

    return [data]

def generate(data):
    verify_arguments(data)

    return str(
        svg(view_box=(0, 0, 200, 100), xmlns="http://www.w3.org/2000/svg")(
            ellipse(cx=100, cy=50, rx=100, ry=50)
        )
    )
    # Outputs this:
    #
    # """
    # <svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    #   <ellipse cx="100" cy="50" rx="100" ry="50" />
    # </svg>
    # """


def verify_arguments(data):
    if(data[0]) is '': data[0] = '🚀'

    assert data[0] is not '', "Please add an emoji"
    assert data[1] is not '', "Please add the version number"