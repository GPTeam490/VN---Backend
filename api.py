import os
import json
import google.generativeai as genai 

# Configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

# Function to generate recommendations based on inputs
def get_recommendations(city, month, time_needed):
    prompt = (f"Generate a structured list of recommendations for {city} in {month}. "
              f"Include activities that fit within {duration}. The output should "
              f"be a JSON file with fields: 'activity', 'best_season', and 'time_needed'.")
    
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            },
        ]
    )

    response = chat_session.send_message(prompt)
    
    # Parse the response
    recommendations = response.text
    
    # Save the response as a JSON file named recommendations.json
    with open('recommendations.json', 'w') as file:
        json.dump(recommendations, file, indent=4)

# TODO: This is an example of values, replace with values we get from front end
if __name__ == "__main__":
    city = "San Francisco"
    month = "October"
    duration = "3 days"

    get_recommendations(city, month, duration)
