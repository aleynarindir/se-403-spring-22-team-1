import openai

openai.api_key = "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"

# Getting inputs:

print("---")
print("Welcome to the Calorie-Based Meal Suggestor!")
print("---")

gender = input("Type 1 if you are a man, 2 if you are a woman: ")
age = input("Enter your age: ")
weight = input("Enter your weight (in kg): ")
height = input("Enter your height (in cm): ")

print("---")
print("Activity Level Options:")
print("1. Sedentary (little or no exercise)")
print("2. Lightly active (light exercise/sports 1-3 days/week)")
print("3. Moderately active (moderate exercise/sports 3-5 days/week)")
print("4. Very active (hard exercise/sports 6-7 days/week)")
print("5. Extra active (very hard exercise/sports & a physical job)")

activity = input("Please select your activity level: ")

print("---")

# Calculation of Harris-Benedict Equation:

def harris_benedict_equation(gender, age, weight, height):
    
    if gender == '1':
        bmr = 66.5 + (13.75 * float(weight)) + (5.003 * float(height)) - (6.75 * float(age))
    elif gender == '2':
        bmr = 665.1 + (9.563 * float(weight)) + (1.850 * float(height)) - (4.676 * float(age))
    else:
        print("Invalid gender entered.")
        return None
    
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
        print("Invalid activity level entered.")
        return None

    return calories

# Giving information:

caloriesInput = int(harris_benedict_equation(gender, age, weight, height))

print("Your needed calories are: " + str(int(harris_benedict_equation(gender, age, weight, height))))
print("---")
print("ChatGPT response:")
print("---")

# ChatGPT API connection and print:

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Suggest a total of exactly " + str(caloriesInput) + " kcal meals as breakfast, lunch and dinner."}])
print(completion.choices[0].message.content)
