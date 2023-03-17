import os
import openai


class ChatApp:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        #openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = OPEN_AI_KEY
        self.messages = [
            {"role": "system", "content": "You are a content expert to help read and understand text and create articles."},
        ]

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        print(response['usage']['total_tokens'])
        print("tokens")

        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]


