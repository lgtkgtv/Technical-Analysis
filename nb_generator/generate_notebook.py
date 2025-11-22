# generate_notebook.py

import os
import json
import nbformat
from google import genai
from google.genai.errors import APIError

# --- Configuration ---
# Use the PRO model for complex structured output like code/JSON
# MODEL_NAME = 'gemini-2.5-pro'
MODEL_NAME = 'gemini-3-pro-preview'
OUTPUT_FILE = 'ma_backtest_notebook.ipynb'

# --- The Prompt ---
# This system instruction guides Gemini to output a perfectly structured JSON file.
SYSTEM_INSTRUCTION = (
    "You are an expert AI/ML developer specializing in secure, educational coding tutorials. "
    "Your task is to generate the content for a complete, working Jupyter Notebook file (.ipynb) in JSON format. "
    "The output must be a single JSON object that strictly adheres to the nbformat V4 specification. "
    "The tutorial should be interactive, using clear Markdown cells for explanation and Python code cells for logic. "
    "Every function called from the yfinance, pandas, numpy etc imported libraries shall be explained when it's called for the first time " 
    "Also explain python code constructs (like list complrhension) that are difficult for C programmers who are new to python"
    "Focus on the 50-day/200-day Moving Average Crossover Backtesting tutorial logic, including fetching data, "
    "calculating MAs, generating signals, calculating returns, and plotting the results using Matplotlib/Plotly. "
    "Do not include any external comments like '[Image of X]' in the final JSON output, as the notebook should "
    "generate its own visualizations. The final notebook must be ready to run."
    "Explain all the concepts finance and technical analysis domain concept using simple visual illustrations, use anologies, example data tables, plots etc as if teaching a 12 year old"
    "As an example this URL is an example of a good and useful chart `https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQOCGxjHHW-CunVvdD7oF_4vPYytYV2FAuc1GNIgLLszng93Y6JREZqd72YkZ0xL_bmQ228ESSD_UK1QmHFcx7p1KRHOF7kYdy6glormtXBJyYH6hI`" 
)

USER_PROMPT = """
Generate a complete Jupyter Notebook tutorial for a 50-day/200-day Moving Average (MA) Crossover Strategy backtest using Python, pandas, and yfinance.
The notebook must have the following sequential sections:
1. Title and Introduction (Markdown).
2. Setup and Dependency Import (Code).
3. Data Fetching and Cleanup (Code + Markdown explanation).
4. MA Calculation and Signal Generation (Code + Markdown explanation).
5. Backtest Logic: Strategy Returns and Equity Curve Calculation (Code + Markdown explanation).
6. Visualization: Plotting the Crossovers and the Equity Curve (Code + Markdown explanation).
7. Final Summary and Interpretation (Markdown).
"""

def generate_notebook_content():
    """Generates notebook content using Gemini and returns it as a dictionary."""
    if not os.getenv("GEMINI_API_KEY"):
        print("🚨 FATAL: GEMINI_API_KEY is not set.")
        return None

    try:
        # Client setup
        client = genai.Client()

        print(f"-> Generating content with model: {MODEL_NAME}...")
        
        # Call Gemini to generate the structured notebook JSON
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=USER_PROMPT,
            config={"system_instruction": SYSTEM_INSTRUCTION}
        )
        
        # Attempt to parse the JSON response text
        # We strip surrounding text that often accompanies structured output (e.g., ```json...```)
        json_text = response.text.strip()
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]

        content_dict = json.loads(json_text.strip())
        
        print("-> Content generated and successfully parsed as JSON.")
        return content_dict
        
    except APIError as e:
        print(f"\nAPI Error: Could not reach Gemini or API key is invalid.")
        print(e)
        return None
    except json.JSONDecodeError as e:
        print("\nError: Gemini did not return valid JSON.")
        print(f"JSON Parsing Error: {e}")
        # Optionally print the raw text to debug why parsing failed
        # print(f"Raw response text was: \n{response.text}")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return None

def write_notebook_file(notebook_data):
    """Writes the JSON content to an .ipynb file."""
    try:
        # Use nbformat library to validate and write the notebook
        nb = nbformat.from_dict(notebook_data)
        nbformat.write(nb, OUTPUT_FILE)
        print(f"\n✅ Success! Fully runnable Jupyter Notebook saved as **{OUTPUT_FILE}**")
        print("To run the notebook:")
        print("1. Install Jupyter: uv pip install notebook matplotlib plotly")
        print("2. Launch: jupyter notebook")
    except Exception as e:
        print(f"Error writing notebook file: {e}")

if __name__ == '__main__':
    notebook_json = generate_notebook_content()
    if notebook_json:
        write_notebook_file(notebook_json)
