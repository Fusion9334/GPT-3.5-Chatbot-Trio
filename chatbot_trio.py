from collections import deque
import openai
import pyttsx3
import random

# Set OpenAI API key
openai.api_key = "APY Key"
MAX_TOKENS = 3750
MAX_MEMORY_CHARACTERS = 15000
MAX_MEMORY_MESSAGES = 100

class LimitedMemoryDeque(deque):
    def __init__(self, maxlen, max_characters):
        super().__init__(maxlen=maxlen)
        self.max_characters = max_characters
        self.total_characters = 0

    def append(self, item):
        super().append(item)
        self.total_characters += len(item["content"])

        while self.total_characters > self.max_characters:
            removed_item = self.popleft()
            self.total_characters -= len(removed_item["content"])

def adaptive_off_topic_chance(memory):
    off_topic_base_chance = 0.30
    recent_questions = [msg["content"] for msg in memory if msg["role"] == "user" and msg["content"].startswith("John,")]
    off_topic_questions = sum(1 for q in recent_questions if "off-topic" in q)
    
    return off_topic_base_chance / 2 if off_topic_questions >= 3 else off_topic_base_chance

def generate_response(memory, user_message, previous_message, model_info):
    humor_instruction = " Include a joke in my response on the subject." if random.random() < 0.15 else ""
    story_instruction = " Include a short story in my response on the subject." if random.random() < 0.5 else ""

    conversation = [{"role": "system", "content": f"I am {model_info['name']}, Model {model_info['number']}. My task is to {model_info['role']} and address other models.{humor_instruction}{story_instruction}"}] + list(memory) + [user_message, previous_message]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)

    return response['choices'][0]['message']

def speak(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.say(text)
    engine.runAndWait()

def handle_model_1(subject, off_topic_chance):
    content = f"John, please ask a similar topic question on the same subject the other models talked about." if random.random() < off_topic_chance else f"John, please ask another question on the subject {subject}."
    return content

def handle_model_2(response_content):
    return f"Sarah, please answer this question: {response_content}"

def handle_model_3(response_content):
    return f"Michael, please give another point of view on this answer: {response_content}"

def main():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    for index, voice in enumerate(voices):
        print(f"{index}: {voice.id} - {voice.name}")
    memories = LimitedMemoryDeque(maxlen=MAX_MEMORY_MESSAGES, max_characters=MAX_MEMORY_CHARACTERS)
    model_infos = [
        {"number": 1, "name": "John", "role": "ask questions on the subject", "voice_id": 0},
        {"number": 2, "name": "Sarah", "role": "answer John's questions", "voice_id": 1},
        {"number": 3, "name": "Michael", "role": "analyze Sarah's response and give another point of view on the subject", "voice_id": 2},
    ]
    subject = input("Enter a conversational subject for the chatbots to talk about: ")
    user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
    previous_message = user_message
    model_number = 0  # Start with the first model (John)

    while True:
        model_response = generate_response(memories, user_message, previous_message, model_infos[model_number])

        if model_number == 0:
            off_topic_chance = adaptive_off_topic_chance(memories)
            content = handle_model_1(subject, off_topic_chance)
            model_number = 1
        elif model_number == 1:
            content = handle_model_2(model_response['content'])
            model_number = 2
        else:
            content = handle_model_3(model_response['content'])
            model_number = 0

        memories.append(model_response)

        speak(model_response['content'], model_infos[model_number]['voice_id'])
        print(f"{model_infos[model_number]['name']}: {model_response['content']}")

        user_message = {"role": "user", "content": content}
        previous_message = model_response

if __name__ == "__main__":
    main()
