import os
import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv


# Check if running on Streamlit Cloud
if "STREAMLIT_RUNTIME" in os.environ:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI client
client = OpenAI(api_key=api_key)

# Load environment variables
load_dotenv()


def generate_prayer(problem_description):
    """Generate a prayer using OpenAI API based on the user's problem"""

    system_prompt = """You are a knowledgeable Catholic assistant. Based on the user's problem, 
    select the most appropriate Catholic saint known for interceding in similar situations. 
    Then compose a brief, heartfelt prayer asking for that saint's intercession. 
    The response should include:
    1. The chosen saint's name and why they are relevant
    2. A 3-4 sentence prayer asking for their intercession, written in the first person (e.g. ""St. Anthony, please help me find my lost keys."")
    Format the response with the saint explanation first, followed by the prayer in italics.
    3. End the prayer with a traditional Catholic closing statement followed by ""Amen."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": problem_description},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Streamlit UI
st.title("Catholic Saint Prayer Generator")
st.write(
    """
Share your concern or problem below, and receive a personalized prayer 
through the intercession of a relevant saint.
"""
)

# Input text area
user_input = st.text_area(
    "Describe your situation:",
    height=100,
    placeholder="Example: I'm struggling with anxiety about an upcoming job interview...",
)

# Generate button
if st.button("Generate Prayer", type="primary"):
    if user_input:
        with st.spinner("Generating your prayer..."):
            prayer = generate_prayer(user_input)
            st.markdown(prayer)
    else:
        st.warning("Please describe your situation first.")

# Sidebar with information
st.sidebar.title("About")
st.sidebar.write(
    """
This app helps you connect with Catholic saints who can intercede for your specific needs. 
It suggests an appropriate saint based on your situation and generates a meaningful prayer 
for their intercession.
"""
)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <small>Remember that this tool is meant to supplement, not replace, 
        your personal prayer life and relationship with God.</small>
    </div>
    """,
    unsafe_allow_html=True,
)
