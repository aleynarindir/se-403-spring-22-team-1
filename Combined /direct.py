from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Load OpenAI language model
openai.api_key = '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'
model_engine = "text-davinci-003"  # Replace with your model engine ID

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# BMR Calculator page
@app.route('/BMRpage.html')
def bmr_calculator():
    return render_template('BMRpage.html')

# AJAX endpoint to get meal recommendations
@app.route('/get_meal_recommendations', methods=['POST'])
def get_meal_recommendations():
    # Get user input from text area
    user_input = request.form['user_input']
    user_input = user_input + "Format suggested meals with a leading '-' ."

    # Call OpenAI API to generate meal recommendations
    meal_recommendations = generate_meal_recommendations(user_input)

    # Return meal recommendations as JSON response
    return jsonify({'meal_recommendations': meal_recommendations})

# Function to generate meal recommendations using OpenAI API
def generate_meal_recommendations(user_input):
    # Call OpenAI API to generate meal recommendations
    response = openai.Completion.create(
      engine=model_engine,
      prompt=user_input,
      temperature=0.5,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    # Extract the generated text from the response
    meal_recommendations = response.choices[0].text.strip()
    meal_rec_list = []

    for meal in meal_recommendations.split("-")[1:]:
        meal_rec_list.append(" - "+meal)

    meal_recommendations = meal_rec_list

    return meal_recommendations

# Harris-Benedict Equation Calculator page
@app.route('/harris_benedict_equation')
def harris_benedict_equation():
    return render_template('harris_benedict_equation.html')

# Results page
@app.route('/results', methods=['POST'])
def results():
    gender = request.form['gender']
    age = request.form['age']
    weight = request.form['weight']
    height = request.form['height']
    activity = request.form['activity']

    # Calculate the daily calorie intake based on Harris-Benedict equation
    caloriesInput = harris_benedict_equation_calculation(gender, age, weight, height, activity)

    # Call OpenAI API to generate meal plan suggestions
    prompt = "Suggest a total of exactly " + str(caloriesInput) + " kcal meals as breakfast, lunch and dinner."
    response = ""

    if prompt:
        response = generate_text(prompt)

    return render_template('results.html', response=response)

# Function to calculate the daily calorie intake based on Harris-Benedict equation
def harris_benedict_equation_calculation(gender, age, weight, height, activity):
    if gender == '1':
        bmr = 66.5 + (13.75 * float(weight)) + (5.003 * float(height)) - (6.75 * float(age))
    elif gender == '2':
        bmr = 665.1 + (9.563 * float(weight)) + (1.850 * float(height)) - (4.676 * float(age))
    else:
        raise ValueError("Invalid gender entered.")
    if activity == '1':
     calories = bmr * 1.2
    elif activity == '2':
     calories = bmr * 1.375
    elif activity == '3':
     calories = bmr * 1.55
    elif activity == '4':
     calories = bmr * 1.725
    elif activity == '5':
     calories = bmr * 1.9
    else:
     raise ValueError("Invalid activity level entered.")

    return calories


def generate_text(prompt):
# Call OpenAI API to generate text based on the prompt using the specified language model
 completion = openai.Completion.create(engine=model_engine, prompt=prompt, temperature=0.7, max_tokens=1000)
 choices = sorted(completion.choices, key=lambda x: x.text.count('\n'), reverse=True)
 response = choices[0].text.strip()
 return response

if __name__ == '__main__':
    app.run(debug=True)

