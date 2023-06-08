# VoiceGPT
ChatGPT + TTS (Eleven Labs version) for windows

In order to get this working properly we have to download and install the following:

1.Python: Ensure that you have Python installed on your system. You can download the latest stable version of Python from the official Python website (https://www.python.org/downloads/) and follow the installation instructions.

2.Python Libraries: Install the following Python libraries by running the following commands in your terminal or command prompt:
<pre>
<code>
Copy code
pip install openai
pip install requests
pip install questionary
pip install elevenlabs
</code>
</pre>
These commands will install the required libraries: openai, requests, questionary, and elevenlabs.

Now we have to setup the py file:

1.Create an account on OpenAI and ElevenLabs and get your API Key using this link: https://platform.openai.com/account/api-keys (The usage can generate a fee)

2. Replace the values in Ln15 & 16 by entering your API Keys 

<pre>
<code>
openai_api_key = "ENTER_YOUR_OPENAI_API_KEY_HERE"
eleven_api_key = "ENTER_YOUR_ELEVEN_LABS_API_KEY_HERE"

#Keep the quotes  and just replace the text with your API keys
</code>
</pre>

3. Once you execute the .py file remeber to select your trained voice model from ElevenLabs using the arrow keys, then enter your Prompt.

(Despite you can download and run this locally, you need internet connection to get communication with API's and alse be aware of the usage).

By having Python and the necessary libraries installed, along with a default audio player on your Windows system, you will be able to run the code smoothly and enjoy the playback of the generated MP3 files (which are located in Windows %temp% folder).
