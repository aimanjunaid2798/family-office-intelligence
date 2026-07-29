import json

from openai import OpenAI

from app.discovery.prompts import SYSTEM_PROMPT


class OllamaClient:

    def __init__(self, model="qwen2.5:7b"):
        self.model = model

        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

    def classify(
        self,
        user_prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0,
    ):

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        return json.loads(content)