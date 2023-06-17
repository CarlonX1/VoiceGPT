import os
import openai
import tempfile
from IPython.display import Audio, clear_output
import speech_recognition as sr
from elevenlabs import generate, play, set_api_key, voices, Models
from dotenv import dotenv_values
import questionary
from pydub import AudioSegment
from pydub.playback import play as play_audio
import msvcrt
import requests
from datetime import datetime

os.environ['SDL_AUDIODRIVER'] = 'dsp'

# Load environment variables from .env file
env = dotenv_values('.env')

openai_api_key = "ENTER_YOUR_OPENAI_API_KEY_HERE"
eleven_api_key = "ENTER_YOUR_ELEVENLABS_API_KEY_HERE"

# Configure GPT-4 and Text-to-speech API keys
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVEN_API_KEY)

voice_list = voices()

voice_labels = [voice.category + " voice: " +
                voice.name for voice in voice_list]

selected_voice_id = questionary.select(
    'Select a voice:',
    choices=voice_labels
).ask()

chatgpt_model = "gpt-3.5-turbo"

chatgpt_system = "You are a helpful assistant in a conversation. Your answer should not be too long. Be ironic and sarcastic."

selected_voice_index = voice_labels.index(selected_voice_id)
selected_voice_id = voice_list[selected_voice_index].voice_id

def transcribe_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    print("Transcribing audio...")
    try:
        prompt = recognizer.recognize_google(audio)
        return prompt
    except sr.UnknownValueError:
        print("Error: Unable to transcribe audio.")
        return ""
    except sr.RequestError:
        print("Error: Unable to connect to Google Speech Recognition API.")
        return ""

def get_gpt4_response(prompt):
    response = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "system", "content": chatgpt_system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def interact_with_gpt4(prompt, conversation):
    response_text = get_gpt4_response(prompt)
    conversation.append({"role": "User", "content": prompt, "timestamp": datetime.now().replace(microsecond=0)})
    conversation.append({"role": "Assistant", "content": response_text, "timestamp": datetime.now().replace(microsecond=0)})
    return response_text


def generate_audio_file(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + selected_voice_id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 1.0
        }
    }

    response = requests.post(url, json=data, headers=headers)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
        f.flush()
        temp_filename = f.name

    return temp_filename

def play_audio_file(audio_file):
    sound = AudioSegment.from_mp3(audio_file)
    play_audio(sound)

def continuous_interaction():
    conversation = []
    while True:
        clear_output(wait=True)
        print("Press 'v' to transcribe audio, 't' to enter a text prompt, or 's' to select a different voice (or 'exit' to stop): ")
        key = msvcrt.getch().decode()
        if key.lower() == 'exit':
            break
        elif key.lower() == 'v':
            prompt = transcribe_audio()
        elif key.lower() == 't':
            prompt = input("Enter your text prompt: ")
        elif key.lower() == 's':
            selected_voice_id = questionary.select(
                'Select a voice:',
                choices=voice_labels
            ).ask()
            selected_voice_index = voice_labels.index(selected_voice_id)
            selected_voice_id = voice_list[selected_voice_index].voice_id
            print("Voice selection updated.")
            continue
        else:
            print("Invalid key. Please try again.")
            continue
        if prompt.lower() == 'exit':
            break
        response_text = interact_with_gpt4(prompt, conversation)
        audio_file = generate_audio_file(response_text)
        play_audio_file(audio_file)

        # Save transcription
        transcript_file = "transcript.txt"
        with open(transcript_file, "w") as file:
            for entry in conversation:
                role = entry["role"]
                content = entry["content"]
                timestamp = entry["timestamp"]
                file.write(f"({timestamp}) {role}: {content}\n")

        print("Conversation transcript saved to transcript.txt")

continuous_interaction()
