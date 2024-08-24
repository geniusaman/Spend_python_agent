import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import io
import traceback
from PIL import Image
import datetime
import time
import os
import base64
from agents.openai_agent import PandasAgentOpenAI

import logging
# Configure logging
logging.basicConfig(filename='logs/csv_agent.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

api_key = st.secrets["openai"]["OPENAI_API_KEY"]

st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #ffffff; /* White background */
    }
    .stApp {
        background-color: #ffffff; /* White background */
    }
    .main-content {
        flex: 1;
        overflow-y: auto; /* Scrollable content */
        padding-bottom: 60px; /* Space for the fixed footer */
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.2);
        color: #000000;
    }
    .title {
        color: #5e17eb; /* Purple title */
        text-align: left;
        font-size: 30px;
        margin-top: 20px; /* Adjust margin-top as needed */
        margin-bottom: 10px; /* Adjust margin-bottom as needed */
    }
    .prompt-input {
        width: 100%;
        border: 1px solid #5e17eb; /* Purple border */
        border-radius: 10px;
        padding: 10px;
        color: #5e17eb; /* Purple text */
        background-color: #f3e9ff; /* Light purple background */
    }
    .prompt-input::placeholder {
        color: #5e17eb; /* Purple color for placeholder text */
    }
    .submit-button {
        background-color: #5e17eb; /* Purple */
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
    }
    .submit-button:hover {
        background-color: #4b13ba; /* Darker purple */
    }
    .reset-button {
        background-color: #5e17eb; /* Purple */
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
    }
    .reset-button:hover {
        background-color: #4b13ba; /* Darker purple */
    }
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 300px; /* Adjust the width as needed */
        height: auto;
        margin-bottom: 20px; /* Adjust margin-bottom as needed */
        border: 2px solid #5e17eb; /* Border around the logo */
        border-radius: 20px; /* Rounded corners */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* Shadow effect */
    }
    .logo-bot{
        display: block;
        margin-left: 10px;
        margin-right: auto;
        width: 25px; /* Adjust the width as needed */
        height: 25px;
        margin-bottom: auto; /* Adjust margin-bottom as needed */
    }
    .logo-bot1{
        display: block;
        margin-left: auto;
        margin-right: 10px;
        width: 30px; /* Adjust the width as needed */
        height: 30px;
        margin-bottom: auto; /* Adjust margin-bottom as needed */
    }
    .input-text {
        color: #5e17eb; /* Purple text */
        font-size: 18px;
        margin-top: 5px; /* Adjust margin-top as needed */
        margin-bottom: 5px; /* Adjust margin-bottom as needed */
    }
    .result-text {
        background-color: #e5dff7; /* Light purple background */
        color: #5e17eb; /* Purple text */
        padding: 10px;
        border-radius: 10px;
        font-size: 18px;
        margin-top: 10px;
    }
    .colored-label {
        color: #5e17eb; /* Purple color for label */
        font-size: 16px;
        margin-bottom: 5px;
    }
    .user-msg {
        background-color: #bab5f6; /* Light purple background */
        padding: 10px;
        border-radius: 10px;
        text-align: right;
        margin-bottom: 10px;
        width: 70%;
        margin-left: auto;
        color: #5e17eb; /* Purple text */
        font-weight: 550;
    }
    .ai-msg {
        background-color: #e7eaf6; /* Light purple background */
        padding: 10px;
        border-radius: 10px;
        text-align: left;
        margin-bottom: 10px;
        width: 70%;
        color: #5e17eb; /* Purple text */
    }
    .session-button {
        background-color: #5e17eb; /* Purple */
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
        text-align: left;
        width: 100%;
    }
    .session-button:hover {
        background-color: #4b13ba; /* Darker purple */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("EaseAi Chatbot")
st.markdown("<h1 class='input-text'><b>🤖 Ask a question about the spend data</b></h1>", unsafe_allow_html=True)

logo_path = "logo.png"
image = Image.open(logo_path)
image = image.resize((280, 80))
if os.path.exists(logo_path):
    st.sidebar.image(image, use_column_width=False)
else:
    st.error(f"Logo file not found at {logo_path}")
sidebar_option = st.sidebar.selectbox(
    "Select Model",
    ("gpt-4o-mini", "claude-haiku")
)

temperature = st.sidebar.slider('Select Temperature', min_value=0.0, max_value=1.0, value=0.1, step=0.1)

csv_agent = PandasAgentOpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Enter your question"):
    st.session_state.messages.append({"role": "user", "content": {"query": prompt}})

if prompt:
    reply, python_code = csv_agent.run_agent(prompt)
    if "plot_data" in reply:
        LLM_reply = reply
        st.session_state.messages.append({"role": "assistant", "content": LLM_reply, "code": python_code})
    else:
        LLM_reply = csv_agent.LLM_response(reply, python_code, prompt)
        st.session_state.messages.append({"role": "assistant", "content": LLM_reply, "code": python_code})
   

for  message in st.session_state.messages:
    if message["role"] == "user":
        logo_url = "https://icons.veryicon.com/png/o/miscellaneous/two-color-icon-library/user-286.png"
        st.markdown(f"<img src='{logo_url}' class='logo-bot1'>", unsafe_allow_html=True)
        st.markdown(f"<div class='user-msg'>{message['content']['query']}</div>", unsafe_allow_html=True)
    else:
        if "plot_data" in message["content"]:
            plot_data = message["content"].get("plot_data", None)
            if plot_data is not None:
                plot_data = plot_data[0]
                image_data = base64.b64decode(plot_data)
                image = Image.open(io.BytesIO(image_data))
                st.image(image)
                with st.expander("Show Code"):
                    st.code(message["code"], language="python")
                
            
        else:
            logo_url = "https://github.com/grv13/LoginPage-main/assets/118931467/aaac9655-af61-4d10-a569-4cd8e382280d"
            st.markdown(f"<img src='{logo_url}' class='logo-bot'>", unsafe_allow_html=True)
            st.markdown(f"<div class='ai-msg'>{message['content']}</div>", unsafe_allow_html=True)
            with st.expander("Show Code"):
                st.code(message["code"], language="python")
        # # # Display the "Show Code" option
        # # if "code" in message:
        #     with st.expander("Show Code"):
        #         st.code(message['assistant']["code"], language="python")
                
