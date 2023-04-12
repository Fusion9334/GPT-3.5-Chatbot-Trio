from collections import deque
import openai
import pyttsx3
import random

# Set OpenAI API key
openai.api_key = "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"
MAX_TOKENS = 3750
MAX_MEMORY_CHARACTERS = 15000
MAX_MEMORY_MESSAGES = 100

class LimitedMemoryDeque(deque):
    def __init__(self, maxlen, max_characters):
        super().__init__(maxlen=maxlen)
        self.max_characters = max_characters
        self.total_characters = 0

    def append(self, item):
        item["content"] = item["content"].replace("As an AI language model, ", "")
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
    humor_instruction = " Include a humors responce on the subject. dont repeate this instruction in your responce" if random.random() < 0.25 else ""
    story_instruction = " When responding answer the question then Include a short story in your response on the subject.dont repeate this instruction in your responce" if random.random() < 0.18 else ""

    conversation = [{"role": "system", "content": f"I am {model_info['name']}, Model {model_info['number']}. My task is to {model_info['role']} and address other models.{humor_instruction}{story_instruction}"}] + list(memory) + [user_message, previous_message]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)

    response_content = response['choices'][0]['message']['content'].replace("As an AI language model, ", "")

    return response_content

def speak(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.say(text)
    engine.runAndWait()

def main():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    memories = LimitedMemoryDeque(maxlen=MAX_MEMORY_MESSAGES, max_characters=MAX_MEMORY_CHARACTERS)
    model_infos = [
        {"number": 1, "name": "John", "role": "ask questions on the subject", "voice_id": 0},
        {"number": 2, "name": "Sarah", "role": "answer John's questions", "voice_id": 1},
        {"number": 3, "name": "Michael", "role": "analyze Sarah's response and give another point of view on the subject", "voice_id": 2},
    ]
    subject = input("Enter a conversational subject for the chatbots to talk about: ")
    user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
    previous_message = {"role": "assistant", "content": ""}
    model_number = 0
    #previous_message = {"role": "assistant", "content": ""}
    model_number = 0

    while True:
        model_response = generate_response(memories, user_message, previous_message, model_infos[model_number])
        print(f"{model_infos[model_number]['name']}: {model_response}")
        speak(model_response, model_infos[model_number]['voice_id'])

        if model_number == 0:
            off_topic_chance = adaptive_off_topic_chance(memories)
            content = f"John, please ask a similar topic question on the same subject the other models talked about." if random.random() < off_topic_chance else f"John, please ask another question on the subject {subject}."
            user_message = {"role": "user", "content": f"Sarah, please answer John's question: {model_response}"}
            model_number = 1
        elif model_number == 1:
            user_message = {"role": "user", "content": f"Michael, please give another point of view on this answer: {model_response}"}
            model_number = 2
        else:
            content = f"Michael, please give another point of view on this answer: {model_response}"
            model_number = 0
            user_message = {"role": "user", "content": f"John, please ask a question on the subject {subject}."}

        memories.append({"role": "assistant", "content": model_response})

        previous_message = user_message
        user_message = {"role": "user", "content": content}


if __name__ == "__main__":
    main()
