import re
from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask import Flask, request, jsonify

os.environ["GOOGLE_API_KEY"] = "AIzaSyCUICsoK71QO6dbRlNDXLILrTRwrCdU-eA"
load_dotenv()  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return ''.join([chunk.text for chunk in response])

app = Flask(__name__)

# Store chat history
chat_history = []

def preprocess_input(user_input):
    # Convert to lowercase
    user_input = user_input.lower()
    # Remove special characters
    user_input = re.sub(r'[^a-z\s]', '', user_input)
    # Split into an array of words
    words = user_input.split()
    return words

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    data = request.json
    user_input = data.get('input')

    if user_input:
        words = preprocess_input(user_input)

        if len(set(words) & {"swaasthaya","tell","swasthaya", "swaasthya","swasthya","what"}) >= 2:
            bot_response = ("Swaasthya is a system designed to help hospitals manage patient care, appointments, and bed availability more efficiently. It makes it easier for hospitals to keep track of everything, reduce wait times, and use their resources better. It’s user-friendly and can even work offline, making it a practical tool for improving hospital operations.")

        elif len(set(words) & {"manage","manages", "patient", "patients", "bed"}) >= 2:
            bot_response = ("Swaasthya manages patient admission and bed availability by tracking beds in real-time and "
                            "categorizing them by type (General, ICU, NICU, Isolation). Hospital staff can update "
                            "available slots for each department, ensuring resources are used efficiently. The system "
                            "links departments to beds and OPD services, making patient admission and bed assignments "
                            "smooth and accurate.")
        elif len(set(words) & {"customizing", "customize", "custom"}) >= 1:
            bot_response = ("Yes, Swaasthya can be customized to fit hospital requirements. It allows for adjustments in "
                            "appointment scheduling, bed management, and departmental setups to match the specific needs "
                            "of each hospital. This flexibility ensures that the system can be tailored to efficiently handle "
                            "different hospital operations and workflows.")
        elif len(set(words) & {"manages", "managing", "opd"}) >= 2:
            bot_response = ("Swaasthya optimizes queuing in OPDs by managing appointment slots effectively. It tracks the "
                            "number of available slots in each department and allows hospital staff to update them in real-time. "
                            "This helps in reducing wait times by ensuring that appointments are scheduled efficiently, and patients "
                            "are seen promptly. The system also categorizes and links OPD services with specific departments, further "
                            "streamlining the patient flow and minimizing delays.")
            
        elif len(set(words) & {"reduce","reduces", "finance", "cost"}) >= 1:
            bot_response = ("Swaasthya cuts operational costs by simplifying hospital processes. It efficiently manages patient admissions, bed availability, and appointments, ensuring that resources like beds and staff are used wisely. This reduces unnecessary spending and helps the hospital operate more smoothly, ultimately saving money.")
            
        elif len(set(words) & {"easy", "staff", "simple"}) >= 2:
            bot_response = ("Swaasthya makes implementation easy with simple dropdowns and minimal data entry. It also works offline, syncing data automatically when the connection is restored, so users can operate smoothly even without internet access.")
        
        elif len(set(words) & {"safe", "secure", "data"}) >= 1:
            bot_response = ("Swaasthya ensures data security by requiring an extra layer of verification after three failed login attempts—on the fourth attempt, users must enter both their password and an OTP. Additionally, if a user is inactive for 15 minutes, the system automatically logs them out to prevent unauthorized access. These features, along with encryption, keep patient data safe and secure.")
        
        elif len(set(words) & {"opd", "slot", "book", "appointment", "how"}) >= 3:
            bot_response = ("To book a slot, visit the Appointments section on the website, select your preferred department (e.g., General Medicine, Cardiology), choose an available time slot, and complete the booking form.")


        elif len(set(words) & {"bed", "slot", "admit", "available", "how", "availability"}) >= 2:
            bot_response = ("Navigate to the Bed Availability section on the homepage to view real-time information on the availability of beds in different departments.")

        elif len(set(words) & {"opd", "slot", "time", "what"}) >= 2:
            bot_response = ("OPD appointments are available in 30-minute slots from 9:00 AM to 5:00 PM, Monday to Saturday. You can check specific slot availability in the Appointments section.")

        elif len(set(words) & {"opd", "slot", "status", "appointment", "how"}) >= 2:
            bot_response = ("Visit the My Appointments page, log in with your credentials, and view the status of your booked appointments.")

        elif len(set(words) & {"review", "service", "feedback", "how"}) >= 2:
            bot_response = ("Use the Contact Us page to submit feedback or inquiries. Alternatively, you can use the chatbot on the bottom right corner of the screen for instant assistance")
        






        else:
            
            bot_response = get_gemini_response(user_input)

        # Remember Sessions
        chat_history.append(("You", user_input))
        chat_history.append(("Bot", bot_response))

        return jsonify({"response": bot_response, "chat_history": chat_history})

    return jsonify({"error": "No input provided"}), 400

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)
