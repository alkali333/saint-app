import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import re
import urllib.parse

# Check if running on Streamlit Cloud
if "STREAMLIT_RUNTIME" in os.environ:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI client
client = OpenAI(api_key=api_key)

# Load environment variables
load_dotenv()


def clean_json_string(text):
    """Clean the response to extract only the JSON part"""
    # Find the first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No valid JSON found in response")
    return text[start : end + 1]


def parse_response(response_text):
    """Parse and validate the JSON response"""
    try:
        # Clean the response text first
        json_str = clean_json_string(response_text)
        # Parse JSON
        data = json.loads(json_str)

        # Validate required fields
        if not isinstance(data, dict):
            raise ValueError("Response is not a JSON object")
        required_fields = {"saint_name", "introduction", "prayer"}
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields in JSON response")

        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")


def create_google_search_link(saint_name):
    """Create a Google search link for the saint"""
    query = urllib.parse.quote(f"Saint {saint_name}")
    return f"https://www.google.com/search?q={query}"


def format_response(data):
    """Format the response with proper markdown"""
    saint_name = data["saint_name"]
    introduction = data["introduction"]
    prayer = data["prayer"]
    search_link = create_google_search_link(saint_name)

    return f"{introduction}\n\n*{prayer}*\n\n[Learn more about Saint {saint_name}]({search_link})"


def generate_prayer(problem_description):
    """Generate a prayer using OpenAI API based on the user's problem"""

    system_prompt = """You are a knowledgeable Catholic assistant. Based on the user's problem, 
    select the most appropriate Catholic saint known for interceding in similar situations. 
    Provide your response in JSON format with these exact fields:
    {
        "saint_name": "Name of the saint only",
        "introduction": "A paragraph explaining why this saint is relevant to the situation",
        "prayer": "A 4-5 sentence prayer asking for their intercession, written in first person, 
                  ending with a traditional Catholic closing statement and Amen"
    }
    
    Example response:
    {
        "saint_name": "Anthony of Padua",
        "introduction": "Saint Anthony of Padua is known as the patron saint of lost items and lost souls. His own life was marked by a miraculous recovery of stolen prayer books, leading to his patronage of lost things.",
        "prayer": "Dear Saint Anthony, please help me in my time of need. Guide my hands and mind to locate what has been lost, and grant me the peace of mind that comes with your intercession. Through Christ our Lord, Amen."
    }"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": problem_description},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        # Parse the response
        parsed_data = parse_response(response.choices[0].message.content)

        # Format the response with proper markdown
        formatted_response = format_response(parsed_data)

        return formatted_response
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
            st.markdown(prayer, unsafe_allow_html=True)
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
st.sidebar.image("luce.png", caption="Image of Luce")

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
