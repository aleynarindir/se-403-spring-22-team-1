# Importing Gradio library for interface options.

import openai
import gradio as gr

# Set up the OpenAI API key
openai.api_key = "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"

# Define a function to generate a 600 kcal breakfast suggestion
def generate_breakfast():
    prompt = "Generate a 600 kcal breakfast suggestion."
    response = openai.Completion.create(
        engine="text-davinci-002",# Testing 'text-davinci-002' instead of 'gpt-3.5-turbo'.
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    suggestion = response.choices[0].text.strip()
    return suggestion

# Define the Gradio interface
interface = gr.Interface(
    fn=generate_breakfast,
    inputs=None,
    outputs=gr.outputs.Textbox(),
    button_text="Generate Breakfast",
    title="600 kcal Breakfast Suggestion"
)

# Launch the interface
interface.launch()
