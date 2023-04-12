# GPT-3.5 Chatbot Trio

This project demonstrates a conversation simulation between three chatbot models, named John, Sarah, and Michael, who use the OpenAI GPT-3.5 Turbo model for generating responses. The chatbots take turns to ask questions, answer them, and give an alternative point of view on the same subject.

## How it works

The main script imports the required libraries, sets up the OpenAI API, and defines functions to handle different aspects of the conversation. The chatbot models follow a predefined conversation flow, and their responses are generated using OpenAI's GPT-3.5 Turbo model.

## Main components

- `resize_memory(memory)`: This function ensures that the total characters in the model's memory do not exceed the specified limit (15,000 characters). It removes the oldest message from memory, except for the question at index 0.

- `generate_response(model_memory, user_message, previous_message, model_info)`: This function takes the model's memory, user message, previous message, and model information as input, and generates a response from the GPT-3.5 Turbo model.

- `speak(text, voice_id)`: This function uses the pyttsx3 library to convert the given text to speech using the specified voice.

- `handle_model_1(subject, off_topic_chance)`, `handle_model_2(response_content)`, and `handle_model_3(response_content)`: These functions handle the conversation flow for each of the chatbot models, returning appropriate content for user messages.

- `main()`: This is the main function that initializes the chatbot models, their voices, and memories. It also sets the conversation subject and starts the conversation simulation.

## Usage

Ensure you have the required libraries installed: `openai`, `pyttsx3`, and `random`.

Set your OpenAI API key in the `openai.api_key` variable.

Run the script, and enter a conversational subject for the chatbots to talk about.

The chatbots will start conversing, with their responses being printed on the console and spoken using the `pyttsx3` library.

## Customization

You can customize various aspects of the chatbot conversation, such as the subject, off-topic chance, and the inclusion of stories or humor in the responses. Modify the corresponding variables and functions in the script as needed.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## In-Depth Explanation

In this section, we'll dive deeper into the code to understand how the different components work together.

### `resize_memory(memory)`

The purpose of this function is to limit the total number of characters in a model's memory. It takes the memory as input and iteratively removes the oldest message from memory until the total number of characters is within the specified limit. It avoids removing the latest question asked by Model 1 (John) to preserve context. This ensures that the conversation stays within the memory constraints of the GPT-3.5 Turbo model.

### `generate_response(model_memory, user_message, previous_message, model_info)`

This function is responsible for generating responses from the GPT-3.5 Turbo model. It takes the following input parameters:

- `model_memory`: The memory of the current chatbot model.
- `user_message`: The message provided by the user (or another model) to the current model.
- `previous_message`: The previous message in the conversation.
- `model_info`: Information about the current chatbot model, including its name, number, and role.

It constructs a conversation structure by concatenating the system message, model memory, user message, and previous message. Depending on the random probability, it may also include a short story or a joke in the response. Then, it sends this conversation to the OpenAI API and returns the generated response.

### `speak(text, voice_id)`

This function utilizes the `pyttsx3` library to convert the given text to speech. It takes the text and a voice ID as input, sets the desired voice, and speaks the text aloud.

### `handle_model_x(response_content)`

These three functions manage the conversation flow for each of the chatbot models. They take the content of the previous response as input and return the appropriate content for the user message.

- `handle_model_1(subject, off_topic_chance)`: For Model 1 (John), the function generates a user message with a new question on the given subject, or an off-topic question with a probability defined by `off_topic_chance`.
- `handle_model_2(response_content)`: For Model 2 (Sarah), the function creates a user message asking her to answer the question provided by Model 1 (John).
- `handle_model_3(response_content)`: For Model 3 (Michael), the function generates a user message requesting an alternative point of view on the answer given by Model 2 (Sarah).

### `main()`

The main function initializes the chatbot models, their voices, memories, and sets the conversation subject. It defines the model information for John, Sarah, and Michael, including their names, numbers, roles, and voice IDs.

The conversation simulation loop starts with Model 1 (John) asking a question. Model 2 (Sarah) then answers the question, and Model 3 (Michael) provides an alternative point of view. The loop continues, with the models taking turns to ask questions, answer them, and give alternative perspectives.

The main function manages the conversation flow, user messages, and model memory. It uses the `generate_response()` function to obtain model responses, and the `speak()` function to convert the responses to speech. The conversation progresses as the chatbot models take turns, with their responses being printed on the console and spoken aloud.

You can modify various aspects of the chatbot conversation by adjusting the subject, off-topic chance, and the inclusion of stories or humor in the responses. Simply modify the corresponding variables and functions in the script as needed.
