import requests

def send_message_to_bot(user_input):
    url = "http://127.0.0.1:5000/chat"
    headers = {"Content-Type": "application/json"}
    data = {"input": user_input}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        bot_response = response.json().get("response")
        return bot_response
    else:
        return "Error: Unable to communicate with the bot."

def chat_loop():
    print("Start chatting with the bot (type 'exit' to stop):")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Ending chat. Goodbye!")
            break
        
        bot_response = send_message_to_bot(user_input)
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    chat_loop()
