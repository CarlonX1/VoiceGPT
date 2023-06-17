# VoiceGPT
ChatGPT + TTS (Eleven Labs version) for windows

In order to get this working properly we have to download and install the following:

1.Python: Ensure that you have Python installed on your system. You can download the latest stable version of Python from the official Python website (https://www.python.org/downloads/) and follow the installation instructions. Then install PIP install <pre>
<code>
pip install --upgrade pip
</code>
</pre>

2.Python Libraries: Install the following Python libraries by running the following commands in your terminal or command prompt:
<pre>
<code>
pip install openai speechrecognition elevenlabs python-dotenv questionary pydub requests PyAudio playsound
</code>
</pre>
These commands will install the required libraries: openai, requests, questionary, and elevenlabs.

Now we have to configure the py file:

1.Create an account on OpenAI and ElevenLabs (https://beta.elevenlabs.io/) and get your API Key using this link: https://platform.openai.com/account/api-keys (The usage can generate a fee)

2. Replace the values in Ln15 & 16 by entering your API Keys 

<pre>
<code>
openai_api_key = "ENTER_YOUR_OPENAI_API_KEY_HERE"
eleven_api_key = "ENTER_YOUR_ELEVENLABS_API_KEY_HERE"

#Keep the quotes and just replace the text with your API keys
</code>
</pre>

3. If you check at Ln 34 the GPT model in use is the 3.5-turbo wichi is much cheaper than GPT4, but you can feel free to switch that. 
And by default the Ln 35 comes the following Prompt/system: 
<pre>
<code>
chatgpt_system = "You are a helpful assistant in a conversation. Answers should not be too long. Be ironic and sarcastic."
</code>
</pre>
So you could give instruction to act as a different kind of person just by changing the text inside the quotes.

4. Once you execute the .py file remember  to select your trained voice model from ElevenLabs using the arrow keys, then enter your Prompt by speaking (Using "V" for Voice) or writing (Using "T" for the text) and can also press "S" to select your preferred voice.

(Despite you can download and run this locally, you will always need internet connection to get communication with API's and alse be aware of the usage).

By having Python and the necessary libraries installed, along with a default audio player on your Windows system, you will be able to run the code smoothly and enjoy the playback of the generated MP3 files (which are located in Windows %temp% folder).
