import openai
import pyttsx3
import random

# Set OpenAI API key
openai.api_key = "API Key"
MAX_TOKENS = 3750
MAX_MEMORY_CHARACTERS = 15000

# Function to resize memory to the specified limit while preserving the latest question asked by Model 1
def resize_memory(memory):
    total_characters = sum([len(msg["content"]) for msg in memory])

    while total_characters > MAX_MEMORY_CHARACTERS:
        # Remove the oldest message from memory, except the question at index 0
        if len(memory) > 2:
            removed_message = memory.pop(1)
            total_characters -= len(removed_message["content"])
        else:
            break

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

# New function to handle Model 1 (John)
def handle_model_1(subject, off_topic_chance):
    if random.random() < off_topic_chance:
        content = f"John, please ask an off-topic question on the same subject the other models talked about."
    else:
        content = f"John, please ask another question on the subject {subject}."
    return content

# New function to handle Model 2 (Sarah)
def handle_model_2(response_content):
    return f"Sarah, please answer this question: {response_content}"

# New function to handle Model 3 (Michael)
def handle_model_3(response_content):
    return f"Michael, please give another point of view on this answer: {response_content}"

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

    off_topic_chance = 0.30

    # Continue the conversation simulation
    while True:
        model_response = generate_response(memories[model_number], user_message, previous_message, model_infos[model_number])

        # Update conversation flow control
        if model_number == 0:
            content = handle_model_1(subject, off_topic_chance)
            model_number = 1
        elif model_number == 1:
            content = handle_model_2(model_response['content'])
            model_number = 2
        else:
            content = handle_model_3(model_response['content'])
            model_number = 0

        # Save the response in the model's memory
        memories[model_number].append(model_response)

        # Resize the memory to limit it to 15,000 characters while preserving the latest question asked by Model 1
        resize_memory(memories[model_number])

        # Speak the response
        speak(model_response['content'], model_infos[model_number]['voice_id'])

        # Print the response
        print(f"{model_infos[model_number]['name']}: {model_response['content']}")

        # Update the user message for the next model
        user_message = {"role": "user", "content": content}
        previous_message = model_response

# Run the main function to start the chatbot conversation simulation
if __name__ == "__main__":
    main()
