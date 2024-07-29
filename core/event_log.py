import functools
import json
import asyncio
from llama_cpp import Llama

llm = Llama(
    model_path="../central/mistral-7b-v0.1.Q4_K_M.gguf",
    n_ctx=1500,
)


class EventLog:
    def __init__(self, config: dict):
        self.events = []
        self.config = config
        self.title = "Loading..."
        self.subtitle = "This could take some time :)"

    def add(self, event: dict):
        if event["type"] in self.config["noRepeatEvents"]:
            self.removeOfType(event["type"])
        # Check for key "notify_llm"
        if event.get("notify_llm", False) is not False:
            event.pop("notify_llm", None)
            self.events.append(event)
            self.notify_llm()
        else:
            self.events.append(event)

    def removeOfType(self, type: str):
        self.events = [event for event in self.events if event["type"] != type]

    def notify_llm(self):
        with open("data/prompts/kindle.txt", "r") as f:
            toLlm = f.read()
            for event in self.events:
                print(f"encoding {str(event)}..")
                toLlm += json.dumps(event) + "\n"

        # toLlm += "\nAssistant Response: "
        toLlm += "\nSummary: "
        output = llm(
            toLlm,
            stop=["[/REAL RESPONSE]"],
            echo=False,
            max_tokens=500,
        )
        response = str(output["choices"][0]["text"])
        print(response)
        json_response = json.loads(response)
        self.title = json_response["title"]
        self.subtitle = json_response["subtext"]
        self.events = []
        return response
