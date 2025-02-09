from flask import Flask, jsonify, request, send_file
import openai
from gtts import gTTS
import os

app = Flask(__name__)

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/get_chatgpt_response', methods=['POST'])
def get_chatgpt_response():
    """
    Receives a JSON payload with a 'prompt' key, calls the ChatGPT API,
    converts the returned text to speech using gTTS, saves it as an MP3 file,
    and returns the text response as JSON.
    """
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data['prompt']
    try:
        # Call the ChatGPT API (using gpt-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        chat_response = response.choices[0].message['content'].strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Convert the text response to an MP3 file using gTTS
    tts = gTTS(chat_response, lang="en")
    tts.save("response.mp3")

    return jsonify({"response": chat_response})

@app.route('/audio', methods=['GET'])
def serve_audio():
    """
    Serves the generated MP3 file (response.mp3) so that the ESP32 can stream/play the audio.
    """
    return send_file("response.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
