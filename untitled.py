import wave
import json
import pyaudio
import threading
from vosk import Model, KaldiRecognizer

# Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Initialize Vosk model
model = Model("vosk-model-small-en-us-0.15")
if model is None:
    print("Error: Vosk model not initialized correctly")
    exit(1)

# Global variables
recording = False
frames = []
audio = None  # Initialize audio globally

# Function to record audio and perform speech recognition
def record_and_recognize():
    global recording, frames, audio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    recognizer = KaldiRecognizer(model, RATE)
    recognizer.SetWords(True)

    print("Recording... Press '2' to stop.")

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if 'result' in result:
                for word in result['result']:
                    start_timestamp = word['start']
                    end_timestamp = word['end']
                    print(f"Word: {word['word']}, Start Time: {start_timestamp:.2f}s, End Time: {end_timestamp:.2f}s")

    stream.stop_stream()
    stream.close()
    audio.terminate()

# Function to start recording
def start_recording():
    global recording, frames
    frames = []  # Clear frames
    recording = True
    threading.Thread(target=record_and_recognize).start()

# Function to stop recording
def stop_recording():
    global recording, frames, audio
    recording = False

    if audio is None:
        print("Error: Audio object is not initialized.")
        return

    wf = wave.open("output.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Perform recognition on saved audio file
    recognize_audio("output.wav")

# Function to recognize audio
def recognize_audio(filename):
    wf = wave.open(filename, 'rb')

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != RATE:
        print("Audio file must be WAV format mono PCM at 16000 Hz")
        wf.close()
        return

    recognizer = KaldiRecognizer(model, RATE)
    recognizer.SetWords(True)
    recognized_text = ""
    timestamps = []

    while True:
        data = wf.readframes(CHUNK)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if 'result' in result:
                for word in result['result']:
                    start_timestamp = word['start']
                    end_timestamp = word['end']
                    recognized_text += f"{word['word']} "
                    timestamps.append((word['word'], start_timestamp, end_timestamp))
            elif 'text' in result:
                recognized_text += result['text'] + " "

    final_result = json.loads(recognizer.FinalResult())
    if 'result' in final_result:
        for word in final_result['result']:
            start_timestamp = word['start']
            end_timestamp = word['end']
            recognized_text += f"{word['word']} "
            timestamps.append((word['word'], start_timestamp, end_timestamp))
    elif 'text' in final_result:
        recognized_text += final_result['text'] + " "

    print("\nRecognized Text:")
    print(recognized_text.strip())

    recognized_words = recognized_text.split()
    total_words = len(recognized_words)
    print(f"\nTotal number of words: {total_words}")

    if timestamps:
        print("\nTimestamps:")
        for word, start, end in timestamps:
            print(f"Word: {word}, Start Time: {start:.2f}s, End Time: {end:.2f}s")
    else:
        print("No word-level timestamps available.")

    wf.close()

# Main loop
while True:
    print("Press '1' to start recording, '2' to stop recording and recognize, '0' to exit")
    user_input = input().strip()

    if user_input == '1':
        start_recording()
    elif user_input == '2':
        stop_recording()
    elif user_input == '0':
        print("Exiting...")
        break
    else:
        print("Invalid input. Please press '1', '2', or '0'.")
