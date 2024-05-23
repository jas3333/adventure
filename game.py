import os
import json
import requests

from rich import print


WORKDIR = os.path.dirname(os.path.abspath(__file__))


class GPT:
    # assistant 0 = description model, assistant 1 = chat model
    def __init__(self):

        with open(f"{WORKDIR}/config/config.json") as file:
            self.key = json.load(file)["api_key"]

        with open(f"{WORKDIR}/config/assistants.json") as file:
            self.assistants = json.load(file)

        self.memory = []
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
        self.url = "https://api.openai.com/v1/chat/completions"

        self.assistants_fix()

    def assistants_fix(self) -> None:
        # System content setup as an array for easier editing. Converts back to a string.
        for i in range(len(self.assistants)):
            self.assistants[i]["messages"][0]["content"] = " ".join(self.assistants[i]["messages"][0]["content"])

    def chat(self, input: str) -> str:
        self.assistants[1]["messages"][1]["content"] = input
        response = requests.post(self.url, headers=self.headers, json=self.assistants[1])

        try:
            gpt_response = response.json()["choices"][0]["message"]["content"]
            return gpt_response
        except KeyError as e:
            return f"Error {e}: {response.json()}"


class Player:
    pass


class World:
    def __init__(self, gpt: GPT):
        self.gpt = gpt
        self.current_room = 0

    def get_description(self, input) -> str:
        self.gpt.assistants[0]["messages"][1]["content"] = input
        response = requests.post(self.gpt.url, headers=self.gpt.headers, json=self.gpt.assistants[0])

        try:
            gpt_response = response.json()["choices"][0]["message"]["content"]
            return gpt_response
        except KeyError as e:
            return f"Error {e}: {response.json()}"


def main():
    gpt = GPT()
    world = World(gpt)

    print(world.gpt.chat("Hi"))


if __name__ == ("__main__"):
    main()
