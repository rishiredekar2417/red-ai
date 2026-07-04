from ollama import AsyncClient


class OllamaProvider:

    def __init__(self):
        self.client = AsyncClient(host="http://localhost:11434")

    async def chat(self, messages):

        response = await self.client.chat(
            model="qwen2.5-coder:7b",
            messages=messages,
        )

        return {
            "text": response["message"]["content"]
        }