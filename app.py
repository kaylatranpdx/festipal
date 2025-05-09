from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Predefined festival locations, possibly replace with an external api call later)
festival_locations = {
    "Coachella": "Indio, California",
    "Glastonbury": "Pilton, England",
    "Tomorrowland": "Boom, Belgium",
    "EDC Las Vegas": "Las Vegas, Nevada",
    "Ultra Music Festival": "Miami, Florida",
    "EDC Orlando": "Orlando, Florida",
    "Lollapalooza": "Chicago, Illinois",
    "Burning Man": "Black Rock City, Nevada",
    "Electric Zoo": "New York City, New York",
    "Sziget Festival": "Budapest, Hungary",
    "Rock in Rio": "Rio de Janeiro, Brazil",
    "Afro Nation": "Praia da Rocha, Portugal",
    "Primavera Sound": "Barcelona, Spain",
    "Chicago Blues Festival": "Chicago, Illinois",
    "Montreux Jazz Festival": "Montreux, Switzerland",
    "New Orleans Jazz & Heritage Festival": "New Orleans, Louisiana"
}

def extract_festival_location(user_input):
    #this will take the user input and extract the festival location
    #system_message = "You are a music festival trip AI that is designed to help those that struggle with finding accommodations for these music festivals. You will be given the name of the festival and you will need to extract the location of the festival to find hotels in that area that are close in distance to the festival. Start your message off by 'This is a great festival! It is located in' and then the location of the festival and hotels that are close in distance. Make the message concise and organized."
    system_message = "You are a music festival trip AI that is designed to help those that struggle with finding accommodations for these music festivals. You will be given the name of the festival and you will need to extract the location of the festival to find hotels in that area that are close in distance to the event. Mention the distance from the hotel to the event and a short description of the hotel, and start your message off with 'What a great festival! Here are some hotels that are close in distance.' Make the message concise."
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content":""}
        ],
        temperature=1,
        max_tokens=256,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content    

#this renders the index.html file
@app.route('/')
def home():
    return render_template('index.html')

#this will take the user input and return the chat response 
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['userINPUT']
    chat_response = extract_festival_location(user_input)
    return jsonify({'response': chat_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0',port=port, debug=True)
