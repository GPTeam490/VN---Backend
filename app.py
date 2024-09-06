from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

api_key = "AIzaSyDGJGoexWWH0bbiM0qmLzjrnMqVbcz7-ss"
genai.configure(api_key=api_key)
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

def generate_itinerary(days, location, month):
    prompt = [f"Build me a vacation itinerary for {days} days in {location} in {month}"]
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Retrieve form data
    days = request.form['duration']
    location = request.form['city']
    month = request.form['month']

    # Generate itinerary using the Generative AI model
    itinerary = generate_itinerary(days, location, month)
    clean_itinerary = itinerary.replace('*', '')

    # Pass the itinerary, location, month, and days back to the template
    return render_template('index.html', itinerary=clean_itinerary, city=location, month=month, duration=days)

@app.route('/ourteam')
def ourteam():

    return render_template('ourteam.html')
@app.route('/homepage')
def homepage():
    return render_template('index.html')


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)