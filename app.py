from flask import Flask, request, render_template
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
import os
import re

app = Flask(__name__)

#groq_api_key
groq_api_key = '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'

#Declaring llm model name
llm_diet_planner = ChatGroq(groq_api_key=groq_api_key, model_name='mixtral-8x7b-32768')

#Creating the prompt to be provided
prompt_template_diet_planner = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics','physical_activity', 'goal'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 7 breakfast names, 7 lunch names, 7 dinner names and 5 workout names, "
             "along with ensuring the goal of the person as well,"
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person level of physical activity: {physical_activity}\n"
             "Person goal: {goal}"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods = ['POST', 'GET'])
def recommend():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_nonveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        physical_activity = request.form['physical_activity']
        goal = request.form['goal']

        #Creating llm chain
        chain_resto = LLMChain(llm=llm_diet_planner, prompt=prompt_template_diet_planner)

        #Defining the input dictionary
        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'veg_or_nonveg': veg_or_nonveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'physical_activity': physical_activity,
            'goal': goal
        }

        #Storing the results here
        results = chain_resto.run(input_data)

        #Extracting the different recommendations using regular expressions
        breakfast_names = re.findall(r'Breakfast:(.*?)Lunch:', results, re.DOTALL)
        lunch_names = re.findall(r'Lunch:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workout:', results, re.DOTALL)
        workout_names = re.findall(r'Workout:(.*?)$', results, re.DOTALL)

        #Cleaning up the extracted lists
        breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\n') if name.strip()] if breakfast_names else []
        lunch_names = [name.strip() for name in lunch_names[0].strip().split('\n') if name.strip()] if lunch_names else []
        dinner_names = [name.strip() for name in dinner_names[0].strip().split('\n') if name.strip()] if dinner_names else []
        workout_names = [name.strip() for name in workout_names[0].strip().split('\n') if name.strip()] if workout_names else []

        return render_template('result.html', breakfast_names = breakfast_names, lunch_names = lunch_names, dinner_names = dinner_names, workout_names = workout_names )

    return render_template('index.html')


if __name__=="__main__":
    app.run(debug = True)