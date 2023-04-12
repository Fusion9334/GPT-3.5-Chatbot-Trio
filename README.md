# GPT-3.5-Chatbot-Trio

This project features a conversation between three AI chatbots, built using OpenAI's GPT-3.5-turbo model. The chatbots are named John, Sarah, and Michael, each with a specific role in the conversation. The program also utilizes the `pyttsx3` library to convert the chatbot's text responses into speech, allowing users to listen to the conversation.

## Features
- Utilizes OpenAI's GPT-3.5-turbo model for generating conversation
- Conversations based on a user-defined subject
- Chatbot roles: John (asks questions), Sarah (answers questions), and Michael (provides alternative perspectives)
- Text-to-speech functionality with `pyttsx3`
- Adaptive off-topic prevention

## Installation
### Prerequisites
- Python 3.6 or higher
- An OpenAI API key

### Dependencies
Install the required dependencies using the following command:

```bash
pip install openai pyttsx3
```

### Setup
1. Clone this repository:

```bash
git clone https://github.com/Fusion9334/GPT-3.5-Chatbot-Trio.git
cd GPT-3.5-Chatbot-Trio
```

2. Add your OpenAI API key to the script by replacing the placeholder text `<your_api_key>` in the following line:

```python
openai.api_key = "<your_api_key>"
```

## Usage
Run the script:

```bash
python main.py
```

Enter a conversational subject for the chatbots to talk about when prompted:

```css
Enter a conversational subject for the chatbots to talk about: <your_subject>
```

The chatbots will then start conversing about the chosen subject. Their conversation will be printed to the console, and their responses will be spoken using `pyttsx3`.

To stop the script, press `Ctrl+C` in the console.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

# Code Overview

In this section, we'll provide a detailed overview of the main components of the GPT-3.5-Chatbot-Trio project, explaining how they work together to create a conversation between three AI chatbots.

## Main Components

- `LimitedMemoryDeque`: This is a custom data structure that extends Python's built-in deque. It is used to store the conversation history between the chatbots, with a limit on both the number of messages and the total number of characters stored.

- `adaptive_off_topic_chance`: This function calculates the chance for John (the first chatbot) to request a question on a similar topic, based on the number of recent off-topic questions. This helps in keeping the conversation focused on the subject.

- `generate_response`: This function generates a response for the current chatbot using OpenAI's GPT-3.5-turbo model. It takes the conversation history, user message, previous message, and model information as inputs and returns a chat completion message.

- `speak`: This function uses the `pyttsx3` library to convert the given text into speech. The `voice_id` parameter is used to select the appropriate voice for each chatbot (John, Sarah, or Michael).

- `handle_model_X`: There are three functions (`handle_model_1`, `handle_model_2`, and `handle_model_3`) that handle the conversation flow between the chatbots. Each function corresponds to one of the chatbots and is responsible for generating the user message for the next chatbot.

- `main`: This is the main function that ties everything together. It initializes the chatbot models, `pyttsx3` engine, and conversation history. It also manages the conversation loop, calling the appropriate handler functions and `generate_response` function in each iteration.

## Conversation Flow

The conversation flow is managed using a while loop in the `main` function. In each iteration of the loop, the script follows these steps:

1. Call the `generate_response` function to generate a response for the current chatbot.
2. Call the appropriate `handle_model_X` function to handle the conversation flow and generate the user message for the next chatbot.
3. Append the generated response to the conversation history.
4. Use the `speak` function to convert the generated response into speech.
5. Print the chatbot's name and response to the console.
6. Update the user message and previous message for the next iteration.

The conversation loop continues indefinitely until the user stops the script by pressing Ctrl+C in the console.

## Customization

You can customize the chatbot behavior by modifying the following parameters:

- `MAX_TOKENS`: The maximum number of tokens for a single API call.
- `MAX_MEMORY_CHARACTERS`: The maximum number of characters to store in the conversation history.
- `MAX_MEMORY_MESSAGES`: The maximum number of messages to store in the conversation history.
- `off_topic_base_chance`: The base probability for John to request a question on a similar topic.

## Extending the Chatbot Trio

If you want to add more chatbots or change their roles, you can do so by modifying the `model_infos` list and creating new handler functions. You may also need to update the `generate_response` function to accommodate the changes in the conversation structure.
