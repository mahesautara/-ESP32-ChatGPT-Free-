import os
import subprocess

# Start Xvfb (Virtual Display) with access control disabled
subprocess.Popen(["Xvfb", ":99", "-ac", "-screen", "0", "1024x768x16"])

# Set DISPLAY environment variable so GUI apps know which display to use
os.environ["DISPLAY"] = ":99.0"

# Ensure that the .Xauthority file exists to satisfy Xlib's requirements
xauth_file = os.path.expanduser("~/.Xauthority")
if not os.path.exists(xauth_file):
    with open(xauth_file, "w") as f:
        pass

# Now import the rest of the modules that rely on the virtual display
from flask import Flask, jsonify, send_file
import pyautogui
import pyperclip
import time
from gtts import gTTS

app = Flask(__name__)

@app.route('/get_chatgpt_response', methods=['GET'])
def get_chatgpt_response():
    """Automates ChatGPT web interface and retrieves response."""
    
    chat_response = ""

    print("Waiting for ChatGPT response...")
    time.sleep(10)  # Ensure ChatGPT has responded before copying

    # Click where ChatGPT's response starts (avoiding the question)
    pyautogui.click(x=629, y=331)
    time.sleep(1)

    while True:
        # Select a portion of the text response
        pyautogui.mouseDown(x=629, y=331)
        time.sleep(0.5)
        pyautogui.moveTo(x=900, y=331)
        pyautogui.mouseUp()
        time.sleep(0.5)

        # Copy the selected text to the clipboard
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)

        copied_text = pyperclip.paste().strip()
        print(f"DEBUG: Copied Text: '{copied_text}'")

        # If the copied text is empty or already included, break the loop
        if copied_text in chat_response or copied_text == "":
            break

        chat_response += " " + copied_text
        # Scroll down slightly to reveal additional text if available
        pyautogui.scroll(-5)
        time.sleep(1)

    print(f"DEBUG: Full Response: {chat_response}")

    # Convert the full text response to an MP3 using gTTS
    tts = gTTS(chat_response, lang="en")
    tts.save("response.mp3")

    return jsonify({"response": chat_response})

@app.route('/audio')
def serve_audio():
    # Serve the generated audio file
    return send_file("response.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
