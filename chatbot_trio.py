import openai
import pyttsx3
import random

openai.api_key = "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"
MAX_TOKENS = 3750

def generate_response(model_memory, user_message, previous_message, model_info):
    story_instruction = " Include a short story in your response on the subject." if random.random() < 0.5 else ""
    humor_instruction = " Include a joke in your response on the subject." if random.random() < 0.15 else ""
    conversation = [{"role": "system", "content": f"You are {model_info['name']}, Model {model_info['number']}. Your task is to {model_info['role']} and address other models.{humor_instruction}{story_instruction}"}] + model_memory + [user_message, previous_message]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
    return response['choices'][0]['message']

def speak(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.say(text)
    engine.runAndWait()

def main():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.id} - {voice.name}")

    memories = [[], [], []]
    model_infos = [
        {"number": 1, "name": "John", "role": "ask questions on the subject", "voice_id": 0},
        {"number": 2, "name": "Sarah", "role": "answer John's questions", "voice_id": 1},
        {"number": 3, "name": "Michael", "role": "analyze Sarah's response and give another point of view on the subject", "voice_id": 2},
    ]

    subject = input("Enter a conversational subject for the chatbots to talk about: ")
    user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
    previous_message = user_message
    model_number = 0  # Make the leader (John) talk first

    while True:
        model_response = generate_response(memories[model_number], user_message, previous_message, model_infos[model_number])
        memories[model_number].extend([user_message, previous_message, model_response])
        memories[model_number] = memories[model_number][-2 * MAX_TOKENS:]
        print(f"{model_infos[model_number]['name']}: {model_response['content']}")
        speak(model_response['content'], model_infos[model_number]['voice_id'])

        previous_message = model_response
        user_role = "user"
        if model_number == 0:
            content = f"Sarah, please answer this question: {model_response['content']}"
            model_number = 1
        elif model_number == 1:
            content = f"Michael, please give another point of view on this answer: {model_response['content']}"
            model_number = 2
        else:
            content = f"John, please ask another question on the subject {subject}."
            model_number = 0
        user_message = {"role": user_role, "content": content}

if __name__ == "__main__":
    main()
