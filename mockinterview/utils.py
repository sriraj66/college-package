from openai import OpenAI
import json

class MockInter:
    def __init__(self, key, role, messages=None) -> None:
        self.prompt = ""
        self.key = key
        self.client = OpenAI(api_key=self.key)
        self.role = role
        self.default_messages = [
                {
                    "role": "system",
                    "content": f"You are an Interviewer named Neuraa AI. Ask questions related to the role '{role}' with a moderate difficulty level. Conduct a maximum of 4 conversations and a minimum of 3 conversations with the user. Questions should be relevant to the role."
                },
                {
                    "role": "system",
                    "content": f"Output must be in the following structured JSON format: {self.ft_template()}"
                },
                {
                    "role": "system",
                    "content": "If you decide to end the interview, set 'is_ended' to true and provide a concise ending note of a maximum of 4 lines."
                },
                {
                    "role": "system",
                    "content": "Start with a self-introduction."
                },
                {
                    "role": "system",
                    "content": "When 'is_ended' is true, provide a rating out of 10 based on the user's skill and behavior in the conversation. The default rating is 1, and the maximum rating is 10. Also, provide a description and advice (minimum 1 line each). Dont leave Empty."
                }
            ]

        self.messages = messages if messages else self.default_messages.copy()

    def ft_template(self):
        return {
        "ai": "Question Topic",
        "question": "Describe the question in 2-6 sentences. You can ask related to the topic or from previous answers.",
        "error": "Provide an error message if there is any misinformation, else None.",
        "is_ended": False,
        "rating": "If is_ended, give a rating out of 10 (dtype<int>). The rating depends on the user's skill and behavior in the previous conversation. Default rating is 1, maximum rating is 10.",
        "description": "If is_ended, give a description about the conversation (minimum 1 line).",
        "advice": "If is_ended, give advice to improve (minimum 1 line).",
    }


    def make_con(self, text):
        if text:
            self.messages.append({"role": "user", "content": text})
        return self.generate()

    def generate(self):
        print("Generating...")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=self.messages,
                response_format={ "type": "json_object" },
                
            )
            if response and response.choices:
                message_content = response.choices[0].message.content
                self.messages.append({"role": "system", "content": message_content})
                print(self.messages)
                
                return message_content
            else:
                raise ValueError("Invalid response from OpenAI API")
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            self.messages.append({"role": "system", "content": "No Answer"})
            return error_message
