# Catholic Saint Prayer Generator

This application helps you connect with Catholic saints who can intercede for your specific needs. It suggests an appropriate saint based on your situation and generates a meaningful prayer for their intercession using the OpenAI API.

## Features

- Suggests a Catholic saint based on your problem description.
- Generates a personalized prayer asking for the saint's intercession.
- Built with Streamlit for a user-friendly interface.

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Run the Streamlit application:**

    ```sh
    streamlit run app.py
    ```

2. **Open your web browser and go to:**

    ```
    http://localhost:8501
    ```

3. **Describe your situation in the text area and click "Generate Prayer" to receive a personalized prayer.**

## Best Practices

- **Environment Variables:** Store sensitive information such as API keys in environment variables. Use the `python-dotenv` package to load these variables from a `.env` file.
- **Virtual Environment:** Use a virtual environment to manage dependencies and avoid conflicts with other projects.
- **Error Handling:** Ensure proper error handling to provide meaningful feedback to the user in case of issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.