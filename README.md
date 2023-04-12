# GPT-3.5 Chatbot Trio

This Python script demonstrates an AI-powered chatbot conversation simulation using the OpenAI API and text-to-speech technology with pyttsx3. Three chatbot models take turns discussing a user-defined subject, each fulfilling a specific role in the conversation. The chatbots ask questions, provide answers, and give alternative points of view, occasionally including jokes or short stories in their responses. This interactive, multi-chatbot experience showcases the potential of AI in generating human-like conversations, making it an excellent foundation for developing engaging voice assistants or chat-based applications optimized for search engine visibility.

## Dependencies

To run this script, you need to install the following libraries:

- openai: OpenAI's official Python library to access GPT models.
- pyttsx3: A text-to-speech library for Python.

You can install these libraries using pip:

```bash
pip install openai pyttsx3
```

## API Key

To use this script, you need to have a valid OpenAI API key. You can obtain one by signing up for an [OpenAI account](https://beta.openai.com/signup/) here.

Replace the following line in the script with your own API key:

```python
openai.api_key = "your-api-key-here"
```

## How it works

The script initializes three chatbots with different roles:

- John: Asks questions on the given subject.
- Sarah: Answers John's questions.
- Michael: Analyzes Sarah's responses and gives another point of view on the subject.

The script uses GPT-4's `openai.ChatCompletion.create()` method to generate responses based on the conversation history and user inputs.

Each chatbot has its own memory, where the latest 2 * MAX_TOKENS messages are stored. This helps the chatbots to maintain context throughout the conversation.

The script also utilizes the pyttsx3 library to provide each chatbot with a different voice, making the conversation more engaging and interactive.

## Usage

Run the script:

```bash
python chatbot_trio.py
```

Enter a conversational subject when prompted:

```css
Enter a conversational subject for the chatbots to talk about: [Your Subject]
```

The chatbots will start conversing based on their roles, and you can listen to the conversation using the selected text-to-speech voices.

## Customization

You can customize the chatbot trio by modifying the `model_infos` list in the script. Each dictionary in the list represents a chatbot and contains the following keys:

- `number`: A unique identifier for the chatbot.
- `name`: The chatbot's name.
- `role`: A brief description of the chatbot's role in the conversation.
- `voice_id`: An index corresponding to the available voices in the pyttsx3 library.

You can experiment with different roles, names, and voices to create a personalized chatbot experience.


# GPT-4 Chatbot Trio - Detailed Explanation

This document provides a detailed explanation of the GPT-4 Chatbot Trio script, including its components and functions.

## Main Components

### Import Libraries
The script imports the necessary libraries to interact with OpenAI's API and to provide text-to-speech functionality:

```python
import openai
import pyttsx3
import random
```

### Set API Key
The script sets the OpenAI API key to authenticate requests to the API:

```python
openai.api_key = "your-api-key-here"
```

Replace "your-api-key-here" with your actual OpenAI API key.

### Constants
MAX_TOKENS is a constant representing the maximum number of tokens to be stored in the chatbots' memories:

```python
MAX_TOKENS = 3750
```

## Functions

### generate_response
This function generates a response for the chatbot based on the model_memory, user_message, previous_message, and model_info parameters:

```python
def generate_response(model_memory, user_message, previous_message, model_info):
    ...
```

The function uses the GPT-4 model with openai.ChatCompletion.create() and returns the generated response.

### speak
This function speaks the given text using the specified voice_id:

```python
def speak(text, voice_id):
    ...
```

The function uses the pyttsx3 library to initialize the engine, set the voice, say the text, and run the text-to-speech engine.

### main
The main function initializes the chatbots, sets their memories, and starts the conversation loop:

```python
def main():
    ...
```

## Chatbot Initialization
The script initializes three chatbots with different roles, names, and voices:

```python
model_infos = [
    {"number": 1, "name": "John", "role": "ask questions on the subject", "voice_id": 0},
    {"number": 2, "name": "Sarah", "role": "answer John's questions", "voice_id": 1},
    {"number": 3, "name": "Michael", "role": "analyze Sarah's response and give another point of view on the subject", "voice_id": 2},
]
```

## Conversation Loop
The conversation loop starts with the user inputting a subject for the chatbots to discuss. The loop continues as the chatbots take turns generating and speaking responses based on their roles and the conversation history.

```python
while True:
    ...
```

The generate_response function is called to produce responses, and the speak function is used to vocalize them using the text-to-speech engine.

## Memory Management
Each chatbot has its own memory to store the conversation history:

```python
memories = [[], [], []]
```

The latest 2 * MAX_TOKENS messages are stored in each chatbot's memory to maintain context during the conversation.

## Customization
You can customize the chatbot trio by modifying the model_infos list in the script. Experiment with different roles, names, and voices to create a personalized chatbot experience.
