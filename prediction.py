import numpy as np
import librosa
from tensorflow.keras.models import model_from_json
import pickle

# Step 1: Load the model
with open('model_files/CNN_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()
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
    # Extract features from audio data
    zcr_feat = zcr(data, frame_length, hop_length)
    rmse_feat = rmse(data, frame_length, hop_length)
    mfcc_feat = mfcc(data, sr, frame_length, hop_length)
    
    # Total expected features length
    max_length = 2376
    
    # Concatenate all features
    result = np.concatenate((zcr_feat, rmse_feat, mfcc_feat))
    
    # Pad with zeros if necessary or truncate
    if result.shape[0] < max_length:
        result = np.pad(result, (0, max_length - result.shape[0]))
    else:
        result = result[:max_length]
        
    return result

def get_predict_feat(path):
    # Load a specific duration of audio starting from an offset
    data, s_rate = librosa.load(path, duration=2.5, offset=0.6)
    features = extract_features(data)
    result = np.array(features).reshape(1, 2376)
    scaled_result = scaler2.transform(result)
    final_result = np.expand_dims(scaled_result, axis=2)
    return final_result

# Step 4: Make predictions
def prediction(path1):
    features = get_predict_feat(path1)
    predictions = loaded_model.predict(features)
    y_pred = encoder2.inverse_transform(predictions)
    return y_pred[0][0]  # Return the emotion string directly