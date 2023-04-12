# GPT-4 Chatbot Trio

This Python script demonstrates the use of OpenAI's GPT-4 model to generate an interactive conversation among three chatbots. The chatbots are named John, Sarah, and Michael, each having their own roles and voices.

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
