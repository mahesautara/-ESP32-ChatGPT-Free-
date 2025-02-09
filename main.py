import os
import subprocess

# Start Xvfb (Virtual Display) with access control disabled (-ac)
subprocess.Popen(["Xvfb", ":99", "-ac", "-screen", "0", "1024x768x16"])
# Set the DISPLAY environment variable so GUI-based modules know which display to use
os.environ["DISPLAY"] = ":99.0"

# Ensure that an empty .Xauthority file exists to satisfy Xlib's requirements.
# This prevents warnings like: "Xlib.xauth: warning, no xauthority details available"
xauth_file = os.path.expanduser("~/.Xauthority")
if not os.path.exists(xauth_file):
    with open(xauth_file, "w") as f:
        pass

# Now import modules that depend on the virtual display
from flask import Flask, jsonify, send_file
import pyautogui
import pyperclip
import time
from gtts import gTTS

app = Flask(__name__)

@app.route('/get_chatgpt_response', methods=['GET'])
def get_chatgpt_response():
    """
    Automates the ChatGPT web interface using pyautogui and pyperclip to capture
    the response text, converts the text to speech using gTTS, and returns the text as JSON.
    """
    chat_response = ""

    print("Waiting for ChatGPT response...")
    # Wait for ChatGPT to generate a response (adjust this delay as needed)
    time.sleep(10)

    # Click to focus on the ChatGPT response area (coordinates may need adjustment)
    pyautogui.click(x=629, y=331)
    time.sleep(1)

    while True:
        # Simulate mouse drag to select text starting from (629, 331) to (900, 331)
        pyautogui.mouseDown(x=629, y=331)
        time.sleep(0.5)
        pyautogui.moveTo(x=900, y=331)
        pyautogui.mouseUp()
        time.sleep(0.5)

        # Copy the selected text to the clipboard
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)

        # Retrieve and clean the copied text
        copied_text = pyperclip.paste().strip()
        print(f"DEBUG: Copied Text: '{copied_text}'")

        # If the text is empty or already captured, break the loop
        if copied_text in chat_response or copied_text == "":
            break

        # Append the new text and scroll down a bit to reveal more content
        chat_response += " " + copied_text
        pyautogui.scroll(-5)
        time.sleep(1)

    print(f"DEBUG: Full Response: {chat_response}")

    # Convert the full text response to an MP3 file using gTTS
    tts = gTTS(chat_response, lang="en")
    tts.save("response.mp3")

    return jsonify({"response": chat_response})

@app.route('/audio')
def serve_audio():
    """
    Serves the generated MP3 file (response.mp3) so clients can play the audio.
    """
    return send_file("response.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    # Run the Flask app on all interfaces at port 8080
    app.run(host="0.0.0.0", port=8080)
