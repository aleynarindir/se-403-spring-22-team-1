from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = "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"
model_engine = "text-davinci-003" # specify the OpenAI language model engine

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/results', methods=['POST'])
def results():
    gender = request.form['gender']
    age = request.form['age']
    weight = request.form['weight']
    height = request.form['height']
    activity = request.form['activity']

    # Calculate the daily calorie intake based on Harris-Benedict equation
    caloriesInput = harris_benedict_equation(gender, age, weight, height, activity)

    # Call OpenAI API to generate meal plan suggestions
    prompt = "Suggest a total of exactly " + str(caloriesInput) + " kcal meals as breakfast, lunch and dinner."
    response = ""

    if prompt:
        response = generate_text(prompt)

    return render_template('results.html', response=response)


def harris_benedict_equation(gender, age, weight, height, activity):
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
