from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import string

# Load the transcription file
transcriptions = pd.read_csv(r'C:\Users\swetha\Desktop\speech_to_sign\transcriptions.csv')

app = Flask(__name__)

# Function to remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    data = request.get_json()
    recognized_text = remove_punctuation(data['recognized_text'].strip().lower())  # Remove extra spaces, lowercase, and punctuation

    # Debugging: Print the recognized text
    print(f"Recognized Text (no punctuation): '{recognized_text}'")

    # Search for the video in the transcriptions
    video_file = None
    for _, row in transcriptions.iterrows():
        transcription_text = remove_punctuation(row['transcription'].strip().lower())  # Remove extra spaces, lowercase, and punctuation

        # Debugging: Print the transcription text from CSV
        print(f"Checking Transcription (no punctuation): '{transcription_text}'")

        # Allow partial matching: Check if recognized text is in transcription
        if recognized_text == transcription_text:
            video_file = row['video_title']
            print(f"Match Found: {video_file}")  # Debugging: Print the matching video file
            break

    if video_file:
        # Path to the video files
        video_path = os.path.join('static', 'videos', video_file)
        return jsonify({'video': video_path})
    else:
        print("No matching video found!")  # Debugging: Print when no match is found
        return jsonify({'video': None})

if __name__ == '__main__':
    app.run(debug=True)
