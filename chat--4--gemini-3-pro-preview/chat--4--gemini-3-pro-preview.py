import os
from google import genai
from google.genai import types

# --- Configuration ---
# Ensure you have the GOOGLE_API_KEY environment variable set
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Use the specific identifier for the new model
model_name = "gemini-3-pro-preview" 

# Set the prompt for a complex task
my_prompt = "Tell me everything about the life and teachings of the Sufi mystic and philosopher Ibn al-Arabi"

# --- API Call and Output ---

print(f"Sending prompt to model: {model_name} with HIGH Thinking Level...")

# Generate content
response = client.models.generate_content(
    model=model_name,
    contents=my_prompt,
    # NEW: Use config to set thinking_level for deeper reasoning (Gemini 3 feature)
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.HIGH,
            include_thoughts=True # CRITICAL FIX: Must be True to receive thoughts
        )
    )
)

print("\n--- GEMINI RESPONSE ---")

# Iterate through parts to find thoughts and text
# response.text filters out thoughts, so we must check parts manually
if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if part.thought:
            print(f"--- THOUGHT ---\n{part.text}\n")
        else:
            print(f"--- RESPONSE ---\n{part.text}\n")
else:
    print("No content returned.")

