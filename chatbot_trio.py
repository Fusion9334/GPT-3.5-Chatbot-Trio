from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from collections import deque
import openai, random, re, threading, pygame, os
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from queue import Queue
from gtts import gTTS
from playsound import playsound

pygame.mixer.init()
# Set OpenAI API key


# The rest of the code remains the same until the ChatbotApp class

class ChatbotApp(App):

    def __init__(self, **kwargs):
        super(ChatbotApp, self).__init__(**kwargs)
        pygame.mixer.init()

    def on_send(self, instance):
        self.stop_voice()
        self.responses_queue.queue.clear()

        if self.subject_input.text:
            subject = self.subject_input.text
            self.subject_input.text = ""

            user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
            previous_message = {"role": "assistant", "content": ""}
            model_number = 0

            threading.Thread(target=self.conversation_loop, args=(subject, user_message, previous_message, model_number)).start()

    responses_queue = Queue()
    openai.api_key = "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"
    MAX_TOKENS = 3750   #this is the number of tokens that can be used in a single request
    MAX_MEMORY_CHARACTERS = 15000 #this is the number of characters that can be stored in the memory
    MAX_MEMORY_MESSAGES = 100   #this is the number of messages that can be stored in the memory
    stop_event = threading.Event()
    class LimitedMemoryDeque(deque):
            def __init__(self, maxlen, max_characters):
                super().__init__(maxlen=maxlen)
                self.max_characters = max_characters
                self.total_characters = 0
            #this is a method that is used to append items to the memory
            def append(self, item):
                item["content"] = item["content"].replace("As an AI language model, ", "")
                super().append(item)
                self.total_characters += len(item["content"])
                #this is a while loop that is used to remove items from the memory if the total number of characters exceeds the maximum number of characters
                while self.total_characters > self.max_characters:
                    removed_item = self.popleft()
                    self.total_characters -= len(removed_item["content"])

    def on_next(self, instance):
        self.stop_voice()
        self.responses_queue.queue.clear()
        if self.subject_input.text and not self.continuous_checkbox.active:
            subject = self.subject_input.text
            self.subject_input.text = ""

            user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
            previous_message = {"role": "assistant", "content": ""}
            model_number = 0

            threading.Thread(target=self.conversation_loop, args=(subject, user_message, previous_message, model_number)).start()



    def build(self):
        self.layout = BoxLayout(orientation="vertical")
        self.conversation_history = TextInput(readonly=True, size_hint=(1, 0.6))
        self.layout.add_widget(self.conversation_history)

        self.input_layout = BoxLayout(size_hint=(1, 0.2))
        self.subject_input = TextInput(hint_text="Enter a subject", multiline=False, size_hint=(0.7, 1))
        self.input_layout.add_widget(self.subject_input)
        self.send_button = Button(text="Send", size_hint=(0.3, 1))
        self.send_button.bind(on_press=self.on_send)
        self.input_layout.add_widget(self.send_button)

        self.layout.add_widget(self.input_layout)

        self.options_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        self.talking_style_spinner = Spinner(
            text='Neutral',
            values=('Neutral', 'Friendly', 'Formal', 'Informative', 'Casual', 'Humorous', 'Professional', 'Socratic', 'Enthusiastic', 'Compassionate', 'Simplified'),
            size_hint=(0.4, 1)
        )
        self.options_layout.add_widget(self.talking_style_spinner)
        self.continuous_layout = BoxLayout(orientation="horizontal", size_hint=(0.4, 1))
        self.continuous_checkbox = CheckBox(active=True, size_hint=(0.3, 1))
        self.continuous_layout.add_widget(Label(text="Continuous conversation", size_hint=(0.7, 1)))
        self.continuous_layout.add_widget(self.continuous_checkbox)
        self.options_layout.add_widget(self.continuous_layout)

        self.speech_layout = BoxLayout(orientation="horizontal", size_hint=(0.4, 1))
        self.speech_checkbox = CheckBox(active=True, size_hint=(0.3, 1))
        self.speech_layout.add_widget(Label(text="Speech on/off", size_hint=(0.7, 1)))
        self.speech_layout.add_widget(self.speech_checkbox)
        self.options_layout.add_widget(self.speech_layout)

        self.next_button = Button(text="Next response", size_hint=(0.2, 1))
        self.next_button.bind(on_press=self.on_next)
        self.options_layout.add_widget(self.next_button)

        self.layout.add_widget(self.options_layout)

        self.stop_button = Button(text="Stop", size_hint=(1, 0.1))
        self.stop_button.bind(on_press=self.on_stop)
        self.layout.add_widget(self.stop_button)  # Move the stop_button to the main layout

        return self.layout

    def stop_voice(self):
        pygame.mixer.music.stop()

    def on_stop(self, instance):
        self.stop_event.set()
        self.stop_voice()

    def update_conversation_history(self, name, message):
        self.conversation_history.text += f"{name}: {message}\n"

    def on_send(self, instance):
        subject = self.subject_input.text
        if not subject:
            return
        self.subject_input.text = ""

        user_message = {"role": "user", "content": f"John, please write one question on the subject {subject}."}
        previous_message = {"role": "assistant", "content": ""}
        model_number = 0

        threading.Thread(target=self.conversation_loop, args=(subject, user_message, previous_message, model_number)).start()

    def generate_response(memory, user_message, previous_message, model_info, talking_style):
        conversation = [
            {"role": "system", "content": f"Set the talking style to {talking_style}."},
            {"role": "system", "content": f"I am {model_info['name']}, Model {model_info['number']}. My task is to {model_info['role']} and address other models."}
        ] + list(memory) + [user_message, previous_message]

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)

        response_content = response['choices'][0]['message']['content']

        # Remove everything up to and including the colon
        response_content = re.sub(r'^.*?:\s*', '', response_content)

        return response_content


    def adaptive_off_topic_chance(memory):
        off_topic_base_chance = 0.30
        recent_questions = [msg["content"] for msg in memory if msg["role"] == "user" and msg["content"].startswith("John,")]
        off_topic_questions = sum(1 for q in recent_questions if "off-topic" in q)

        return off_topic_base_chance / 2 if off_topic_questions >= 3 else off_topic_base_chance

    def speak(self, text, voice_id):
        if self.speech_checkbox.active and not self.stop_event.is_set() and text.strip():
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save("temp_audio.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load("temp_audio.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and not self.stop_event.is_set():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()

            os.remove("temp_audio.mp3")



    def conversation_loop(self, subject, user_message, previous_message, model_number):
        model_response = ""
        self.stop_event.clear()
        memories = ChatbotApp.LimitedMemoryDeque(maxlen=ChatbotApp.MAX_MEMORY_MESSAGES, max_characters=ChatbotApp.MAX_MEMORY_CHARACTERS)
        model_infos = [
            {"number": 0, "name": "John", "role": "ask questions on the subject", "voice_id": 0},
            {"number": 1, "name": "Sarah", "role": "answer John's questions.", "voice_id": 1},
            {"number": 2, "name": "Michael", "role": "analyze Sarah's response and give another point of view on the subject.", "voice_id": 2},
        ]

        ask_related_question = True
        while True:
            talking_style = self.talking_style_spinner.text
            model_response = ChatbotApp.generate_response(memories, user_message, previous_message, model_infos[model_number], talking_style)
            Clock.schedule_once(lambda dt: self.update_conversation_history(model_infos[model_number]['name'], model_response))
            ChatbotApp.speak(self, model_response, model_infos[model_number]['voice_id'])

            previous_message = {"role": "assistant", "content": model_response}
            memories.append(previous_message)

            if model_number == 0:
                off_topic_chance = ChatbotApp.adaptive_off_topic_chance(memories)
                content = f"John, please ask a related question about the previous response: {model_response}" if random.random() < off_topic_chance else f"John, please ask a question on the subject {subject}."
                user_message = {"role": "user", "content": f"Sarah, please answer John's question: {model_response}"}
                model_number = 1
            elif model_number == 1:
                user_message = {"role": "user", "content": f"Michael, please give another point of view on this answer: {model_response} and ask a question on the subject {subject}."}
                model_number = 2
            else:
                if ask_related_question:
                    user_message = {"role": "user", "content": f"John, please ask a question related to this response: {model_response} and dont repeat these instructions in your responce"}
                else:
                    user_message = {"role": "user", "content": f"John, please ask a question on the subject {subject} and dont repeat these instructions in your responce"}
                ask_related_question = not ask_related_question

                # Check if the last sentence of the 3rd model's response contains a question mark
                last_sentence = model_response.strip().split('.')[-1]
                if '?' in last_sentence:
                    content = f"Sarah, please answer Michael's question: {last_sentence}"
                    user_message = {"role": "user", "content": content}
                    model_number = 1
                else:
                    content = f"John, please ask a question on the subject {subject}."
                user_message = {"role": "user", "content": content}
                model_number = 1

            # Check if the last sentence of the 3rd model's response contains a question mark
            last_sentence = model_response.strip().split('.')[-1]
            if '?' in last_sentence:
                content = f"Sarah, please answer Michael's question: {last_sentence}"
                user_message = {"role": "user", "content": content}
                model_number = 1

            # Add the current response to the memory
            previous_message = {"role": "assistant", "content": model_response}
            memories.append(previous_message)

            # Check if continuous conversation is turned off
            if not self.continuous_checkbox.active:
                break

            # Check if the stop button was pressed
            if self.stop_event.is_set():
                break

            # Pre-generate the next response while the current one is being played
            talking_style = self.talking_style_spinner.text
            model_response = ChatbotApp.generate_response(memories, user_message, previous_message, model_infos[model_number], talking_style)
            self.responses_queue.put(model_response)





if __name__ == '__main__':
    ChatbotApp().run()
