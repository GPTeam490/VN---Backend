from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure the API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create the model with the required generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


def get_recommendations(city, month, duration):
    prompt = (
        f"Generate a structured list of travel recommendations for {city} in {month}. "
        f"Include activities that fit within {duration}. The output should "
        f"be a JSON array where each item has fields: 'activity', 'best_season', and 'time_needed'."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            },
        ]
    )

    try:
        response = chat_session.send_message(prompt)
        recommendations_text = response.text.strip()

        # Parse the JSON response
        recommendations = json.loads(recommendations_text)

        return recommendations
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        month = request.form.get('month')
        duration = request.form.get('duration')

        recommendations = get_recommendations(city, month, duration)

        if recommendations is not None:
            return render_template('recommendations.html', recommendations=recommendations, city=city, month=month,
                                   duration=duration)
        else:
            error_message = "Failed to fetch recommendations. Please try again."
            return render_template('recommendations.html', error=error_message)
    return render_template('recommendations.html')


if __name__ == '__main__':
    app.run(debug=True)
