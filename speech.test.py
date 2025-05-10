after edit provde me a full code ,i want make improvement on Record Audio functionalty and make it in best practise and professionally, 
and i want after show the resuilt in 'Upload File tab' and click on Record Audio Tab then clear the result of 'Upload File tab' , and do the same for 
Record Audio tab


│   app.py
│   prediction.py
│
├───model_files
│       best_model1_weights.h5
│       CNN_model.json
│       CNN_model_weights.h5
│       encoder2.pickle
│       scaler2.pickle
│
├───templates
│   │   contact.php
│   │   index.html
│   │   index.php
│   │   indexx.html
│   │   login.php
│   │   logout.php
│   │   Node.js
│   │   register.php
│   │   sample.php
│   │
│   ├───css
│   │       style.css
│   │
│   ├───img
│   │       llogo.png
│   │       log.svg
│   │       logo.png
│   │       logo.svg
│   │       nurse-talking-to-disabled-and-happy-senior-scaled.jpg
│   │       register.svg
│   │
│   ├───include
│   │       connect.php
│   │       footer.php
│   │       header.php
│   │       ini.php
│   │
│   └───js
│           aos.js
│           app.js
│           bootstrap.js
│           jq.js
│           main.js
│           popupscript.js
│           sample.php
│           script.js
│
└───uploads
        116973__cbeeching__hat-light.wav
        saas.wav






app.py:
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
        os.remove(file_path)  # Clean up the temporary file
        return jsonify({'emotion': emotion})
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


prediction.py
import numpy as np
import librosa
from tensorflow.keras.models import model_from_json
import pickle

# Step 1: Load the model
json_file = open('model_files/CNN_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Load weights into the model
loaded_model.load_weights('model_files/best_model1_weights.h5')
print("Loaded model from disk")

# Step 2: Load the scaler and encoder
with open('model_files/scaler2.pickle', 'rb') as f:
    scaler2 = pickle.load(f)

with open('model_files/encoder2.pickle', 'rb') as f:
    encoder2 = pickle.load(f)

print("Scaler and encoder loaded successfully")

# Step 3: Define the feature extraction functions
def zcr(data, frame_length, hop_length):
    return np.squeeze(librosa.feature.zero_crossing_rate(data, frame_length=frame_length, hop_length=hop_length))

def rmse(data, frame_length=2048, hop_length=512):
    return np.squeeze(librosa.feature.rms(data, frame_length=frame_length, hop_length=hop_length))

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten=True):
    mfccs = librosa.feature.mfcc(data, sr=sr)
    return np.squeeze(mfccs.T) if not flatten else np.ravel(mfccs.T)

def extract_features(data, sr=22050, frame_length=2048, hop_length=512):
    result = np.array([])
    
    # Extract features
    zcr_feat = zcr(data, frame_length, hop_length)
    rmse_feat = rmse(data, frame_length, hop_length)
    mfcc_feat = mfcc(data, sr, frame_length, hop_length)
    
    # Pad features to ensure consistent length
    max_length = 2376  # Total number of features expected
    
    # Concatenate all features
    result = np.concatenate((zcr_feat, rmse_feat, mfcc_feat))
    
    # Pad with zeros if shorter than expected
    if result.shape[0] < max_length:
        result = np.pad(result, (0, max_length - result.shape[0]))
    # Truncate if longer than expected
    else:
        result = result[:max_length]
        
    return result

def get_predict_feat(path):
    d, s_rate = librosa.load(path, duration=2.5, offset=0.6)  # Load a specific duration of the audio
    res = extract_features(d)
    result = np.array(res)
    result = np.reshape(result, newshape=(1, 2376))  # Ensure the correct shape for the input
    i_result = scaler2.transform(result)  # Scale the features
    final_result = np.expand_dims(i_result, axis=2)  # Add batch dimension
    return final_result

# Step 4: Make predictions
emotions1 = {1: 'Neutral', 2: 'Calm', 3: 'Happy', 4: 'Sad', 5: 'Angry', 6: 'Fear', 7: 'Disgust', 8: 'Surprise'}

def prediction(path1):
    res = get_predict_feat(path1)
    predictions = loaded_model.predict(res)
    y_pred = encoder2.inverse_transform(predictions)
    return y_pred[0][0]  # Return the emotion string directly


index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Recognition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/wavesurfer.js/6.6.3/wavesurfer.min.js"></script>
</head>
<body class="bg-light">
    <div class="container mt-5" style="max-width: 600px;">
        <div class="card shadow">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Audio Emotion Recognition</h2>

                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="upload-tab" data-bs-toggle="tab" href="#upload" role="tab" aria-controls="upload" aria-selected="true">Upload File</a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="record-tab" data-bs-toggle="tab" href="#record" role="tab" aria-controls="record" aria-selected="false">Record Audio</a>
                    </li>
                </ul>

                <div class="tab-content mt-3" id="myTabContent">
                    <!-- File Upload Tab -->
                    <div class="tab-pane fade show active" id="upload" role="tabpanel" aria-labelledby="upload-tab">
                        <form method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <input type="file" class="form-control" name="file" accept=".wav">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Analyze Emotion</button>
                        </form>
                    </div>

                    <!-- Record Audio Tab -->
                    <div class="tab-pane fade" id="record" role="tabpanel" aria-labelledby="record-tab">
                        <div class="mb-3">
                            <button id="recordButton" class="btn btn-danger">Start Recording</button>
                            <button id="stopButton" class="btn btn-secondary" disabled>Stop Recording</button>
                            <p id="recordingTime" class="mt-2">00:00</p>
                        </div>

                        <div id="waveform" class="mb-3"></div>

                        <div class="mb-3">
                            <button id="playButton" class="btn btn-primary" disabled>Play Audio</button>
                            <audio id="audioPlayer" class="form-control mt-2" controls style="display:none;"></audio>
                        </div>

                        <button id="saveButton" class="btn btn-info mb-3">Save Audio</button>

                        <button id="analyzeRecordingButton" class="btn btn-success mb-3" disabled>Analyze Recording</button>
                    </div>
                </div>

                {% if result %}
                    <div class="mt-4 text-center">
                        <h3>Result:</h3>
                        <div class="display-4">{{ result }}</div>
                        <small class="text-muted">File: {{ filename }}</small>
                    </div>
                {% endif %}

                {% if error %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Add Bootstrap JS to handle tab functionality -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>

    <script>
        // Initialize WaveSurfer
        let wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: 'blue',
            progressColor: 'purple',
        });

        // Recording Controls
        let audioContext;
        let mediaStream;
        let isRecording = false;
        let audioChunks = [];
        let currentAudioBuffer = null;
        let audioElement = new Audio();
        let recordingStartTime = null;
        let recordingInterval = null;

        const recordButton = document.getElementById('recordButton');
        const stopButton = document.getElementById('stopButton');
        const playButton = document.getElementById('playButton');
        const saveButton = document.getElementById('saveButton');
        const analyzeRecordingButton = document.getElementById('analyzeRecordingButton');
        const recordingTime = document.getElementById('recordingTime');
        const audioPlayer = document.getElementById('audioPlayer');

        recordButton.addEventListener('click', async () => {
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioContext.createMediaStreamSource(mediaStream);
                const processor = audioContext.createScriptProcessor(4096, 1, 1);

                source.connect(processor);
                processor.connect(audioContext.destination);

                processor.onaudioprocess = (e) => {
                    if (!isRecording) return;
                    const channelData = e.inputBuffer.getChannelData(0);
                    audioChunks.push(new Float32Array(channelData));
                };

                isRecording = true;
                recordingStartTime = Date.now();
                recordingInterval = setInterval(updateRecordingTime, 1000);
                recordButton.disabled = true;
                stopButton.disabled = false;
            } catch (error) {
                console.error('Error accessing microphone:', error);
            }
        });

        function updateRecordingTime() {
            if (!isRecording) return;
            const elapsedTime = Math.floor((Date.now() - recordingStartTime) / 1000);
            const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0');
            const seconds = String(elapsedTime % 60).padStart(2, '0');
            recordingTime.textContent = `${minutes}:${seconds}`;
        }

        stopButton.addEventListener('click', () => {
            isRecording = false;
            mediaStream.getTracks().forEach(track => track.stop());
            clearInterval(recordingInterval);

            const audioData = new Float32Array(audioChunks.reduce((acc, chunk) => acc + chunk.length, 0));
            let offset = 0;
            audioChunks.forEach(chunk => {
                audioData.set(chunk, offset);
                offset += chunk.length;
            });

            currentAudioBuffer = audioContext.createBuffer(1, audioData.length, audioContext.sampleRate);
            currentAudioBuffer.getChannelData(0).set(audioData);
            audioChunks = [];

            const wavBlob = audioBufferToWav(currentAudioBuffer);
            wavesurfer.load(URL.createObjectURL(wavBlob));

            recordButton.disabled = false;
            stopButton.disabled = true;
            playButton.disabled = false;
            saveButton.disabled = false;
        });

        // Save Functionality
        saveButton.addEventListener('click', () => {
            if (!currentAudioBuffer) return;
            const wavBlob = audioBufferToWav(currentAudioBuffer);
            const url = URL.createObjectURL(wavBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'audio.wav';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            analyzeRecordingButton.disabled = false; // Enable analyze button after saving
        });

// Analyze Recording Functionality
analyzeRecordingButton.addEventListener('click', () => {
    const wavBlob = audioBufferToWav(currentAudioBuffer);
    const formData = new FormData();
    formData.append('file', wavBlob, 'audio.wav');

    fetch('/upload-recording', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(`Emotion: ${data.emotion}`);
    })
    .catch(error => console.error('Error analyzing recording:', error));
});


        // Convert Audio Buffer to WAV
        function audioBufferToWav(buffer) {
            const numChannels = buffer.numberOfChannels;
            const length = buffer.length;
            const sampleRate = buffer.sampleRate;
            const bytesPerSample = 2;
            const blockAlign = numChannels * bytesPerSample;
            const bufferSize = length * blockAlign;
            const arrayBuffer = new ArrayBuffer(44 + bufferSize);
            const view = new DataView(arrayBuffer);

            // WAV header
            writeString(view, 0, 'RIFF');
            view.setUint32(4, 36 + bufferSize, true);
            writeString(view, 8, 'WAVE');
            writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, 1, true);
            view.setUint16(22, numChannels, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * blockAlign, true);
            view.setUint16(32, blockAlign, true);
            view.setUint16(34, bytesPerSample * 8, true);
            writeString(view, 36, 'data');
            view.setUint32(40, bufferSize, true);

            // PCM data
            const dataView = new DataView(arrayBuffer, 44);
            let offset = 0;
            for (let i = 0; i < length; i++) {
                for (let channel = 0; channel < numChannels; channel++) {
                    const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
                    const intSample = sample < 0 ? sample * 32768 : sample * 32767;
                    dataView.setInt16(offset, intSample, true);
                    offset += 2;
                }
            }

            return new Blob([view], { type: 'audio/wav' });
        }

        function writeString(view, offset, string) {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        }
    </script>
</body>
</html>after edit provde me a full code ,i want make improvement on Record Audio functionalty and make it in best practise and professionally, 
and i want after show the resuilt in 'Upload File tab' and click on Record Audio Tab then clear the result of 'Upload File tab' , and do the same for 
Record Audio tab


│   app.py
│   prediction.py
│
├───model_files
│       best_model1_weights.h5
│       CNN_model.json
│       CNN_model_weights.h5
│       encoder2.pickle
│       scaler2.pickle
│
├───templates
│   │   contact.php
│   │   index.html
│   │   index.php
│   │   indexx.html
│   │   login.php
│   │   logout.php
│   │   Node.js
│   │   register.php
│   │   sample.php
│   │
│   ├───css
│   │       style.css
│   │
│   ├───img
│   │       llogo.png
│   │       log.svg
│   │       logo.png
│   │       logo.svg
│   │       nurse-talking-to-disabled-and-happy-senior-scaled.jpg
│   │       register.svg
│   │
│   ├───include
│   │       connect.php
│   │       footer.php
│   │       header.php
│   │       ini.php
│   │
│   └───js
│           aos.js
│           app.js
│           bootstrap.js
│           jq.js
│           main.js
│           popupscript.js
│           sample.php
│           script.js
│
└───uploads
        116973__cbeeching__hat-light.wav
        saas.wav






app.py:
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
        os.remove(file_path)  # Clean up the temporary file
        return jsonify({'emotion': emotion})
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


prediction.py
import numpy as np
import librosa
from tensorflow.keras.models import model_from_json
import pickle

# Step 1: Load the model
json_file = open('model_files/CNN_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Load weights into the model
loaded_model.load_weights('model_files/best_model1_weights.h5')
print("Loaded model from disk")

# Step 2: Load the scaler and encoder
with open('model_files/scaler2.pickle', 'rb') as f:
    scaler2 = pickle.load(f)

with open('model_files/encoder2.pickle', 'rb') as f:
    encoder2 = pickle.load(f)

print("Scaler and encoder loaded successfully")

# Step 3: Define the feature extraction functions
def zcr(data, frame_length, hop_length):
    return np.squeeze(librosa.feature.zero_crossing_rate(data, frame_length=frame_length, hop_length=hop_length))

def rmse(data, frame_length=2048, hop_length=512):
    return np.squeeze(librosa.feature.rms(data, frame_length=frame_length, hop_length=hop_length))

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten=True):
    mfccs = librosa.feature.mfcc(data, sr=sr)
    return np.squeeze(mfccs.T) if not flatten else np.ravel(mfccs.T)

def extract_features(data, sr=22050, frame_length=2048, hop_length=512):
    result = np.array([])
    
    # Extract features
    zcr_feat = zcr(data, frame_length, hop_length)
    rmse_feat = rmse(data, frame_length, hop_length)
    mfcc_feat = mfcc(data, sr, frame_length, hop_length)
    
    # Pad features to ensure consistent length
    max_length = 2376  # Total number of features expected
    
    # Concatenate all features
    result = np.concatenate((zcr_feat, rmse_feat, mfcc_feat))
    
    # Pad with zeros if shorter than expected
    if result.shape[0] < max_length:
        result = np.pad(result, (0, max_length - result.shape[0]))
    # Truncate if longer than expected
    else:
        result = result[:max_length]
        
    return result

def get_predict_feat(path):
    d, s_rate = librosa.load(path, duration=2.5, offset=0.6)  # Load a specific duration of the audio
    res = extract_features(d)
    result = np.array(res)
    result = np.reshape(result, newshape=(1, 2376))  # Ensure the correct shape for the input
    i_result = scaler2.transform(result)  # Scale the features
    final_result = np.expand_dims(i_result, axis=2)  # Add batch dimension
    return final_result

# Step 4: Make predictions
emotions1 = {1: 'Neutral', 2: 'Calm', 3: 'Happy', 4: 'Sad', 5: 'Angry', 6: 'Fear', 7: 'Disgust', 8: 'Surprise'}

def prediction(path1):
    res = get_predict_feat(path1)
    predictions = loaded_model.predict(res)
    y_pred = encoder2.inverse_transform(predictions)
    return y_pred[0][0]  # Return the emotion string directly


index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Recognition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/wavesurfer.js/6.6.3/wavesurfer.min.js"></script>
</head>
<body class="bg-light">
    <div class="container mt-5" style="max-width: 600px;">
        <div class="card shadow">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Audio Emotion Recognition</h2>

                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="upload-tab" data-bs-toggle="tab" href="#upload" role="tab" aria-controls="upload" aria-selected="true">Upload File</a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="record-tab" data-bs-toggle="tab" href="#record" role="tab" aria-controls="record" aria-selected="false">Record Audio</a>
                    </li>
                </ul>

                <div class="tab-content mt-3" id="myTabContent">
                    <!-- File Upload Tab -->
                    <div class="tab-pane fade show active" id="upload" role="tabpanel" aria-labelledby="upload-tab">
                        <form method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <input type="file" class="form-control" name="file" accept=".wav">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Analyze Emotion</button>
                        </form>
                    </div>

                    <!-- Record Audio Tab -->
                    <div class="tab-pane fade" id="record" role="tabpanel" aria-labelledby="record-tab">
                        <div class="mb-3">
                            <button id="recordButton" class="btn btn-danger">Start Recording</button>
                            <button id="stopButton" class="btn btn-secondary" disabled>Stop Recording</button>
                            <p id="recordingTime" class="mt-2">00:00</p>
                        </div>

                        <div id="waveform" class="mb-3"></div>

                        <div class="mb-3">
                            <button id="playButton" class="btn btn-primary" disabled>Play Audio</button>
                            <audio id="audioPlayer" class="form-control mt-2" controls style="display:none;"></audio>
                        </div>

                        <button id="saveButton" class="btn btn-info mb-3">Save Audio</button>

                        <button id="analyzeRecordingButton" class="btn btn-success mb-3" disabled>Analyze Recording</button>
                    </div>
                </div>

                {% if result %}
                    <div class="mt-4 text-center">
                        <h3>Result:</h3>
                        <div class="display-4">{{ result }}</div>
                        <small class="text-muted">File: {{ filename }}</small>
                    </div>
                {% endif %}

                {% if error %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Add Bootstrap JS to handle tab functionality -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>

    <script>
        // Initialize WaveSurfer
        let wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: 'blue',
            progressColor: 'purple',
        });

        // Recording Controls
        let audioContext;
        let mediaStream;
        let isRecording = false;
        let audioChunks = [];
        let currentAudioBuffer = null;
        let audioElement = new Audio();
        let recordingStartTime = null;
        let recordingInterval = null;

        const recordButton = document.getElementById('recordButton');
        const stopButton = document.getElementById('stopButton');
        const playButton = document.getElementById('playButton');
        const saveButton = document.getElementById('saveButton');
        const analyzeRecordingButton = document.getElementById('analyzeRecordingButton');
        const recordingTime = document.getElementById('recordingTime');
        const audioPlayer = document.getElementById('audioPlayer');

        recordButton.addEventListener('click', async () => {
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioContext.createMediaStreamSource(mediaStream);
                const processor = audioContext.createScriptProcessor(4096, 1, 1);

                source.connect(processor);
                processor.connect(audioContext.destination);

                processor.onaudioprocess = (e) => {
                    if (!isRecording) return;
                    const channelData = e.inputBuffer.getChannelData(0);
                    audioChunks.push(new Float32Array(channelData));
                };

                isRecording = true;
                recordingStartTime = Date.now();
                recordingInterval = setInterval(updateRecordingTime, 1000);
                recordButton.disabled = true;
                stopButton.disabled = false;
            } catch (error) {
                console.error('Error accessing microphone:', error);
            }
        });

        function updateRecordingTime() {
            if (!isRecording) return;
            const elapsedTime = Math.floor((Date.now() - recordingStartTime) / 1000);
            const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0');
            const seconds = String(elapsedTime % 60).padStart(2, '0');
            recordingTime.textContent = `${minutes}:${seconds}`;
        }

        stopButton.addEventListener('click', () => {
            isRecording = false;
            mediaStream.getTracks().forEach(track => track.stop());
            clearInterval(recordingInterval);

            const audioData = new Float32Array(audioChunks.reduce((acc, chunk) => acc + chunk.length, 0));
            let offset = 0;
            audioChunks.forEach(chunk => {
                audioData.set(chunk, offset);
                offset += chunk.length;
            });

            currentAudioBuffer = audioContext.createBuffer(1, audioData.length, audioContext.sampleRate);
            currentAudioBuffer.getChannelData(0).set(audioData);
            audioChunks = [];

            const wavBlob = audioBufferToWav(currentAudioBuffer);
            wavesurfer.load(URL.createObjectURL(wavBlob));

            recordButton.disabled = false;
            stopButton.disabled = true;
            playButton.disabled = false;
            saveButton.disabled = false;
        });

        // Save Functionality
        saveButton.addEventListener('click', () => {
            if (!currentAudioBuffer) return;
            const wavBlob = audioBufferToWav(currentAudioBuffer);
            const url = URL.createObjectURL(wavBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'audio.wav';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            analyzeRecordingButton.disabled = false; // Enable analyze button after saving
        });

// Analyze Recording Functionality
analyzeRecordingButton.addEventListener('click', () => {
    const wavBlob = audioBufferToWav(currentAudioBuffer);
    const formData = new FormData();
    formData.append('file', wavBlob, 'audio.wav');

    fetch('/upload-recording', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(`Emotion: ${data.emotion}`);
    })
    .catch(error => console.error('Error analyzing recording:', error));
});


        // Convert Audio Buffer to WAV
        function audioBufferToWav(buffer) {
            const numChannels = buffer.numberOfChannels;
            const length = buffer.length;
            const sampleRate = buffer.sampleRate;
            const bytesPerSample = 2;
            const blockAlign = numChannels * bytesPerSample;
            const bufferSize = length * blockAlign;
            const arrayBuffer = new ArrayBuffer(44 + bufferSize);
            const view = new DataView(arrayBuffer);

            // WAV header
            writeString(view, 0, 'RIFF');
            view.setUint32(4, 36 + bufferSize, true);
            writeString(view, 8, 'WAVE');
            writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, 1, true);
            view.setUint16(22, numChannels, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * blockAlign, true);
            view.setUint16(32, blockAlign, true);
            view.setUint16(34, bytesPerSample * 8, true);
            writeString(view, 36, 'data');
            view.setUint32(40, bufferSize, true);

            // PCM data
            const dataView = new DataView(arrayBuffer, 44);
            let offset = 0;
            for (let i = 0; i < length; i++) {
                for (let channel = 0; channel < numChannels; channel++) {
                    const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
                    const intSample = sample < 0 ? sample * 32768 : sample * 32767;
                    dataView.setInt16(offset, intSample, true);
                    offset += 2;
                }
            }

            return new Blob([view], { type: 'audio/wav' });
        }

        function writeString(view, offset, string) {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        }
    </script>
</body>
</html>after edit provde me a full code ,i want make improvement on Record Audio functionalty and make it in best practise and professionally, 
and i want after show the resuilt in 'Upload File tab' and click on Record Audio Tab then clear the result of 'Upload File tab' , and do the same for 
Record Audio tab


│   app.py
│   prediction.py
│
├───model_files
│       best_model1_weights.h5
│       CNN_model.json
│       CNN_model_weights.h5
│       encoder2.pickle
│       scaler2.pickle
│
├───templates
│   │   contact.php
│   │   index.html
│   │   index.php
│   │   indexx.html
│   │   login.php
│   │   logout.php
│   │   Node.js
│   │   register.php
│   │   sample.php
│   │
│   ├───css
│   │       style.css
│   │
│   ├───img
│   │       llogo.png
│   │       log.svg
│   │       logo.png
│   │       logo.svg
│   │       nurse-talking-to-disabled-and-happy-senior-scaled.jpg
│   │       register.svg
│   │
│   ├───include
│   │       connect.php
│   │       footer.php
│   │       header.php
│   │       ini.php
│   │
│   └───js
│           aos.js
│           app.js
│           bootstrap.js
│           jq.js
│           main.js
│           popupscript.js
│           sample.php
│           script.js
│
└───uploads
        116973__cbeeching__hat-light.wav
        saas.wav






app.py:
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
        os.remove(file_path)  # Clean up the temporary file
        return jsonify({'emotion': emotion})
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


prediction.py
import numpy as np
import librosa
from tensorflow.keras.models import model_from_json
import pickle

# Step 1: Load the model
json_file = open('model_files/CNN_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Load weights into the model
loaded_model.load_weights('model_files/best_model1_weights.h5')
print("Loaded model from disk")

# Step 2: Load the scaler and encoder
with open('model_files/scaler2.pickle', 'rb') as f:
    scaler2 = pickle.load(f)

with open('model_files/encoder2.pickle', 'rb') as f:
    encoder2 = pickle.load(f)

print("Scaler and encoder loaded successfully")

# Step 3: Define the feature extraction functions
def zcr(data, frame_length, hop_length):
    return np.squeeze(librosa.feature.zero_crossing_rate(data, frame_length=frame_length, hop_length=hop_length))

def rmse(data, frame_length=2048, hop_length=512):
    return np.squeeze(librosa.feature.rms(data, frame_length=frame_length, hop_length=hop_length))

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten=True):
    mfccs = librosa.feature.mfcc(data, sr=sr)
    return np.squeeze(mfccs.T) if not flatten else np.ravel(mfccs.T)

def extract_features(data, sr=22050, frame_length=2048, hop_length=512):
    result = np.array([])
    
    # Extract features
    zcr_feat = zcr(data, frame_length, hop_length)
    rmse_feat = rmse(data, frame_length, hop_length)
    mfcc_feat = mfcc(data, sr, frame_length, hop_length)
    
    # Pad features to ensure consistent length
    max_length = 2376  # Total number of features expected
    
    # Concatenate all features
    result = np.concatenate((zcr_feat, rmse_feat, mfcc_feat))
    
    # Pad with zeros if shorter than expected
    if result.shape[0] < max_length:
        result = np.pad(result, (0, max_length - result.shape[0]))
    # Truncate if longer than expected
    else:
        result = result[:max_length]
        
    return result

def get_predict_feat(path):
    d, s_rate = librosa.load(path, duration=2.5, offset=0.6)  # Load a specific duration of the audio
    res = extract_features(d)
    result = np.array(res)
    result = np.reshape(result, newshape=(1, 2376))  # Ensure the correct shape for the input
    i_result = scaler2.transform(result)  # Scale the features
    final_result = np.expand_dims(i_result, axis=2)  # Add batch dimension
    return final_result

# Step 4: Make predictions
emotions1 = {1: 'Neutral', 2: 'Calm', 3: 'Happy', 4: 'Sad', 5: 'Angry', 6: 'Fear', 7: 'Disgust', 8: 'Surprise'}

def prediction(path1):
    res = get_predict_feat(path1)
    predictions = loaded_model.predict(res)
    y_pred = encoder2.inverse_transform(predictions)
    return y_pred[0][0]  # Return the emotion string directly


index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Recognition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/wavesurfer.js/6.6.3/wavesurfer.min.js"></script>
</head>
<body class="bg-light">
    <div class="container mt-5" style="max-width: 600px;">
        <div class="card shadow">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Audio Emotion Recognition</h2>

                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="upload-tab" data-bs-toggle="tab" href="#upload" role="tab" aria-controls="upload" aria-selected="true">Upload File</a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="record-tab" data-bs-toggle="tab" href="#record" role="tab" aria-controls="record" aria-selected="false">Record Audio</a>
                    </li>
                </ul>

                <div class="tab-content mt-3" id="myTabContent">
                    <!-- File Upload Tab -->
                    <div class="tab-pane fade show active" id="upload" role="tabpanel" aria-labelledby="upload-tab">
                        <form method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <input type="file" class="form-control" name="file" accept=".wav">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Analyze Emotion</button>
                        </form>
                    </div>

                    <!-- Record Audio Tab -->
                    <div class="tab-pane fade" id="record" role="tabpanel" aria-labelledby="record-tab">
                        <div class="mb-3">
                            <button id="recordButton" class="btn btn-danger">Start Recording</button>
                            <button id="stopButton" class="btn btn-secondary" disabled>Stop Recording</button>
                            <p id="recordingTime" class="mt-2">00:00</p>
                        </div>

                        <div id="waveform" class="mb-3"></div>

                        <div class="mb-3">
                            <button id="playButton" class="btn btn-primary" disabled>Play Audio</button>
                            <audio id="audioPlayer" class="form-control mt-2" controls style="display:none;"></audio>
                        </div>

                        <button id="saveButton" class="btn btn-info mb-3">Save Audio</button>

                        <button id="analyzeRecordingButton" class="btn btn-success mb-3" disabled>Analyze Recording</button>
                    </div>
                </div>

                {% if result %}
                    <div class="mt-4 text-center">
                        <h3>Result:</h3>
                        <div class="display-4">{{ result }}</div>
                        <small class="text-muted">File: {{ filename }}</small>
                    </div>
                {% endif %}

                {% if error %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Add Bootstrap JS to handle tab functionality -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>

    <script>
        // Initialize WaveSurfer
        let wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: 'blue',
            progressColor: 'purple',
        });

        // Recording Controls
        let audioContext;
        let mediaStream;
        let isRecording = false;
        let audioChunks = [];
        let currentAudioBuffer = null;
        let audioElement = new Audio();
        let recordingStartTime = null;
        let recordingInterval = null;

        const recordButton = document.getElementById('recordButton');
        const stopButton = document.getElementById('stopButton');
        const playButton = document.getElementById('playButton');
        const saveButton = document.getElementById('saveButton');
        const analyzeRecordingButton = document.getElementById('analyzeRecordingButton');
        const recordingTime = document.getElementById('recordingTime');
        const audioPlayer = document.getElementById('audioPlayer');

        recordButton.addEventListener('click', async () => {
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioContext.createMediaStreamSource(mediaStream);
                const processor = audioContext.createScriptProcessor(4096, 1, 1);

                source.connect(processor);
                processor.connect(audioContext.destination);

                processor.onaudioprocess = (e) => {
                    if (!isRecording) return;
                    const channelData = e.inputBuffer.getChannelData(0);
                    audioChunks.push(new Float32Array(channelData));
                };

                isRecording = true;
                recordingStartTime = Date.now();
                recordingInterval = setInterval(updateRecordingTime, 1000);
                recordButton.disabled = true;
                stopButton.disabled = false;
            } catch (error) {
                console.error('Error accessing microphone:', error);
            }
        });

        function updateRecordingTime() {
            if (!isRecording) return;
            const elapsedTime = Math.floor((Date.now() - recordingStartTime) / 1000);
            const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0');
            const seconds = String(elapsedTime % 60).padStart(2, '0');
            recordingTime.textContent = `${minutes}:${seconds}`;
        }

        stopButton.addEventListener('click', () => {
            isRecording = false;
            mediaStream.getTracks().forEach(track => track.stop());
            clearInterval(recordingInterval);

            const audioData = new Float32Array(audioChunks.reduce((acc, chunk) => acc + chunk.length, 0));
            let offset = 0;
            audioChunks.forEach(chunk => {
                audioData.set(chunk, offset);
                offset += chunk.length;
            });

            currentAudioBuffer = audioContext.createBuffer(1, audioData.length, audioContext.sampleRate);
            currentAudioBuffer.getChannelData(0).set(audioData);
            audioChunks = [];

            const wavBlob = audioBufferToWav(currentAudioBuffer);
            wavesurfer.load(URL.createObjectURL(wavBlob));

            recordButton.disabled = false;
            stopButton.disabled = true;
            playButton.disabled = false;
            saveButton.disabled = false;
        });

        // Save Functionality
        saveButton.addEventListener('click', () => {
            if (!currentAudioBuffer) return;
            const wavBlob = audioBufferToWav(currentAudioBuffer);
            const url = URL.createObjectURL(wavBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'audio.wav';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            analyzeRecordingButton.disabled = false; // Enable analyze button after saving
        });

// Analyze Recording Functionality
analyzeRecordingButton.addEventListener('click', () => {
    const wavBlob = audioBufferToWav(currentAudioBuffer);
    const formData = new FormData();
    formData.append('file', wavBlob, 'audio.wav');

    fetch('/upload-recording', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(`Emotion: ${data.emotion}`);
    })
    .catch(error => console.error('Error analyzing recording:', error));
});


        // Convert Audio Buffer to WAV
        function audioBufferToWav(buffer) {
            const numChannels = buffer.numberOfChannels;
            const length = buffer.length;
            const sampleRate = buffer.sampleRate;
            const bytesPerSample = 2;
            const blockAlign = numChannels * bytesPerSample;
            const bufferSize = length * blockAlign;
            const arrayBuffer = new ArrayBuffer(44 + bufferSize);
            const view = new DataView(arrayBuffer);

            // WAV header
            writeString(view, 0, 'RIFF');
            view.setUint32(4, 36 + bufferSize, true);
            writeString(view, 8, 'WAVE');
            writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, 1, true);
            view.setUint16(22, numChannels, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * blockAlign, true);
            view.setUint16(32, blockAlign, true);
            view.setUint16(34, bytesPerSample * 8, true);
            writeString(view, 36, 'data');
            view.setUint32(40, bufferSize, true);

            // PCM data
            const dataView = new DataView(arrayBuffer, 44);
            let offset = 0;
            for (let i = 0; i < length; i++) {
                for (let channel = 0; channel < numChannels; channel++) {
                    const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
                    const intSample = sample < 0 ? sample * 32768 : sample * 32767;
                    dataView.setInt16(offset, intSample, true);
                    offset += 2;
                }
            }

            return new Blob([view], { type: 'audio/wav' });
        }

        function writeString(view, offset, string) {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        }
    </script>
</body>
</html>