import openai
import pyttsx3
import random

# Set OpenAI API key
openai.api_key = "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"
MAX_TOKENS = 3750

# Function to generate a response from the AI model
def generate_response(model_memory, user_message, previous_message, model_info):
    # Add story and humor instructions based on random probability
    story_instruction = " Include a short story in my response on the subject." if random.random() < 0.5 else ""
    humor_instruction = " Include a joke in my response on the subject." if random.random() < 0.15 else ""
    
    # Create conversation structure for OpenAI API call
    conversation = [{"role": "system", "content": f"I am {model_info['name']}, Model {model_info['number']}. My task is to {model_info['role']} and address other models.{humor_instruction}{story_instruction}"}] + model_memory + [user_message, previous_message]
    
    # Call OpenAI API to generate a response
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
    
    return response['choices'][0]['message']

# Function to speak the text using the specified voice
def speak(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.say(text)
    engine.runAndWait()

# Main function to run the chatbot conversation simulation
def main():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # List available voices
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.id} - {voice.name}")

    # Initialize memory for each chatbot model
    memories = [[], [], []]
    
    # Define model information and roles
    model_infos = [
        {"number": 1, "name": "John", "role": "ask questions on the subject", "voice_id": 0},
        {"number": 2, "name": "Sarah", "role": "answer John's questions", "voice_id": 1},
        {"number": 3, "name": "Michael", "role": "analyze Sarah's response and give another point of view on the subject", "voice_id": 2},
    ]

        # Get user input for conversation subject
    subject = input("Enter a conversational subject for the chatbots to talk about: ")
    user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
    previous_message = user_message
    model_number = 0  # Start with the first model (John)

    # Continue the conversation simulation
    while True:
        model_response = generate_response(memories[model_number], user_message, previous_message, model_infos[model_number])
        # ... (previous code)

        # Determine which model should respond next
        if model_number == 0:
            off_topic_chance = 0.30
            if random.random() < off_topic_chance:
                content = f"John, please ask an off-topic question on the subject the other midels taked about."
            else:
                content = f"John, please ask another question on the subject {subject}."
            model_number = 1
        elif model_number == 1:
            content = f"Sarah, please answer this question: {model_response['content']}"
            model_number = 2
        else:
            content = f"Michael, please give another point of view on this answer: {model_response['content']}"
            model_number = 0

        # Update the user message for the next model
        user_message = {"role": user_role, "content": content}

# Run the main function to start the chatbot conversation simulation
if __name__ == "__main__":
    main()
