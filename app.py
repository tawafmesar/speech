from flask import Flask, render_template, request, jsonify
from prediction import prediction
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', error='No file selected')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            emotion = prediction(file_path)
            emoji = get_emoji(emotion)
            os.remove(file_path)  # Clean up uploaded file
            return render_template('index.html', result=f"{emotion} {emoji}", filename=file.filename)
    return render_template('index.html')

@app.route('/upload-recording', methods=['POST'])
def upload_recording():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file temporarily for processing
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    file.save(file_path)

    try:
        emotion = prediction(file_path)  # Use prediction logic
        emoji = get_emoji(emotion)
        os.remove(file_path)  # Clean up the temporary file
        return jsonify({'emotion': f"{emotion} {emoji}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_emoji(emotion):
    EMOJI_MAP = {
        'neutral': '😐',
        'calm': '😌',
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'fear': '😨',
        'disgust': '🤢',
        'surprise': '😲'
    }
    return EMOJI_MAP.get(emotion.lower(), '❓')

if __name__ == '__main__':
    app.run(debug=True)