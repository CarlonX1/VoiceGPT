import os
import openai
import tempfile
import requests
from elevenlabs import generate, set_api_key, voices, Models
from dotenv import dotenv_values
import questionary
import subprocess

os.environ['SDL_AUDIODRIVER'] = 'directsound'

# Load environment variables from .env file
env = dotenv_values('.env')

openai_api_key = "ENTER_YOUR_OPENAI_API_KEY_HERE"
eleven_api_key = "ENTER_YOUR_ELEVEN_LABS_API_KEY_HERE"

# Configure GPT-4 and Text-to-speech API keys
openai.api_key = openai_api_key
set_api_key(eleven_api_key)

voice_list = voices()

# Select voice
voice_labels = [voice.category + " voice: " +
                voice.name for voice in voice_list]

selected_voice_id = questionary.select(
    'Select a voice:',
    choices=voice_labels
).ask()

# Configuration for ChatGPT
chatgpt_model = "gpt-3.5-turbo"
chatgpt_system = "You are a helpful assistant in a conversation. Answers should not be too long. Be ironic and sarcastic."

# Find the index of the selected option
selected_voice_index = voice_labels.index(selected_voice_id)
selected_voice_id = voice_list[selected_voice_index].voice_id

# Function to get GPT-4 response
def get_gpt4_response(prompt):
    response = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "system", "content": chatgpt_system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Main function to interact with GPT-4
def interact_with_gpt4(prompt):
    response_text = get_gpt4_response(prompt)

    url = "https://api.elevenlabs.io/v1/text-to-speech/" + selected_voice_id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": eleven_api_key
    }

    data = {
        "text": response_text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 1.0
        }
    }

    response = requests.post(url, json=data, headers=headers)

    # Save audio data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        f.write(response.content)
        temp_filename = f.name

    return temp_filename


# Function to continuously interact with GPT-4
def continuous_interaction():
    while True:
        prompt = input("Enter your prompt (or type 'exit' to stop): ")
        if prompt.lower() == 'exit':
            break
        audio_file = interact_with_gpt4(prompt)
        play_audio_file(audio_file)

def play_audio_file(file_path):
    subprocess.Popen(['start', '', file_path], shell=True)

# Example usage
continuous_interaction()
