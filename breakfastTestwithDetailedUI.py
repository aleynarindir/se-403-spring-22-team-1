# Importing Gradio library for interface.

import gradio as gr
import openai

# Set up OpenAI API credentials

openai.api_key = "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"

# Define function to generate meal suggestions

def generate_meals(gender, age, height, weight, activity_level):
    
    # Calculate daily caloric needs based on provided inputs
    
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    if activity_level == "Sedentary":
        caloric_needs = bmr * 1.2
    elif activity_level == "Moderately Active":
        caloric_needs = bmr * 1.55
    else:
        caloric_needs = bmr * 1.9

    # Generate meal suggestions based on calculated caloric needs:
    
    breakfast_prompt = f"What are some breakfast ideas for someone who needs {int(caloric_needs * 0.25)} calories?"
    lunch_prompt = f"What are some lunch ideas for someone who needs {int(caloric_needs * 0.35)} calories?"
    dinner_prompt = f"What are some dinner ideas for someone who needs {int(caloric_needs * 0.4)} calories?"
    
    # Breakfast:
    
    breakfast = openai.Completion.create(
      engine="text-davinci-002",
      prompt=breakfast_prompt,
      temperature=0.5,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    ).choices[0].text.strip()
    
    # Lunch:
    
    lunch = openai.Completion.create(
      engine="text-davinci-002",
      prompt=lunch_prompt,
      temperature=0.5,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    ).choices[0].text.strip()
    
    # Dinner:

    dinner = openai.Completion.create(
      engine="text-davinci-002",
      prompt=dinner_prompt,
      temperature=0.5,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    ).choices[0].text.strip()

    # Return meal suggestions as output
    return f"For breakfast: {breakfast}\n\nFor lunch: {lunch}\n\nFor dinner: {dinner}"

# Define Gradio interface with text inputs and radio buttons

gender_input = gr.inputs.Radio(choices=["Male", "Female"], label="Gender")
age_input = gr.inputs.Number(label="Age")
height_input = gr.inputs.Number(label="Height (in inches)")
weight_input = gr.inputs.Number(label="Weight (in pounds)")
activity_level_input = gr.inputs.Radio(choices=["Sedentary", "Moderately Active", "Active"], label="Activity Level")

output_text = gr.outputs.Textbox(label="Meal Suggestions")

interface = gr.Interface(fn=generate_meals, inputs=[gender_input, age_input, height_input, weight_input, activity_level_input], 
                         outputs=output_text, 
                         title="Meal Suggestion Generator", 
                         description="Enter your gender, age, height, weight, and activity level to get meal suggestions and estimated daily caloric needs.")

# Launch Gradio interface
interface.launch()
