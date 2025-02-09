from flask import Flask, jsonify, send_file
import pyautogui
import pyperclip
import time
from gtts import gTTS
import os
import subprocess

app = Flask(__name__)

# Start Xvfb (Virtual Display) with access control disabled
subprocess.Popen(["Xvfb", ":99", "-ac", "-screen", "0", "1024x768x16"])
os.environ["DISPLAY"] = ":99.0"

@app.route('/get_chatgpt_response', methods=['GET'])
def get_chatgpt_response():
    """Automates ChatGPT web interface and retrieves response."""
    
    chat_response = ""

    print("Waiting for ChatGPT response...")
    time.sleep(10)  # Ensure ChatGPT has responded before copying

    # Click where ChatGPT's response starts (Avoids the question)
    pyautogui.click(x=629, y=331)
    time.sleep(1)

    while True:
        # Select a portion of the text response
        pyautogui.mouseDown(x=629, y=331)
        time.sleep(0.5)
        pyautogui.moveTo(x=900, y=331)
        pyautogui.mouseUp()
        time.sleep(0.5)

        # Copy the selected text to clipboard
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)

        copied_text = pyperclip.paste().strip()
        print(f"DEBUG: Copied Text: '{copied_text}'")

        # If the copied text is empty or already included, stop the loop
        if copied_text in chat_response or copied_text == "":
            break

        chat_response += " " + copied_text
        # Scroll down slightly to reveal more text if available
        pyautogui.scroll(-5)
        time.sleep(1)

    print(f"DEBUG: Full Response: {chat_response}")

    # Convert the full response text to MP3 using gTTS
    tts = gTTS(chat_response, lang="en")
    tts.save("response.mp3")

    return jsonify({"response": chat_response})

@app.route('/audio')
def serve_audio():
    # Serve the generated audio file
    return send_file("response.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
