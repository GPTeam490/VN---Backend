from flask import Flask, render_template, request
import google.generativeai as genai
import os
app = Flask(__name__)

#genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
api_key = "AIzaSyDGJGoexWWH0bbiM0qmLzjrnMqVbcz7-ss"
genai.configure(api_key=api_key)
generation_config = {"temperature" : 0.9, "top_p": 1, "top_k": 1, "max_output_tokens":2048}

# Initialize the model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

# Function to generate vacation itinerary
def generate_itinerary(days, location, month):
    prompt = [f"Build me a vacation itinerary for {days} days in {location} in {month}"]
    response = model.generate_content(prompt)
    return response.text

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/generate', methods=['POST'])
def generate():
    days = request.form['days']
    location = request.form['location']
    month = request.form['month']
    itinerary = generate_itinerary(days, location, month)
    return render_template('index.html', itinerary=itinerary)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)