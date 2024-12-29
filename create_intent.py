import json

from environs import Env
from google.cloud import dialogflow_v2 as dialogflow

env = Env()
env.read_env()
tg_bot_token = env.str("TG_BOT_TOKEN")
google_project_id = env.str("GOOGLE_PROJECT_ID")

with open("questions.json", encoding="UTF-8") as file:
    intent_phrases = json.load(file)

intent_names = list(intent_phrases.keys())
display_name = intent_names[0]
training_phrases_parts = intent_phrases[display_name]["questions"]
answer = intent_phrases[display_name]["answer"]

intents_client = dialogflow.IntentsClient()

parent = dialogflow.AgentsClient.agent_path(google_project_id)

training_phrases = []

for training_phrases_part in training_phrases_parts:
    part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
    training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
    training_phrases.append(training_phrase)

text = dialogflow.Intent.Message.Text(text=[answer])
message = dialogflow.Intent.Message(text=text)

intent = dialogflow.Intent(
    display_name=display_name,
    training_phrases=training_phrases,
    messages=[message],
)

response = intents_client.create_intent(
    request={"parent": parent, "intent": intent}
)
