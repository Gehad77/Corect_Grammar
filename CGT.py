# Import the necessary libraries and models
from faster_whisper import WhisperModel  # Audio-to-Text model
from happytransformer import HappyTextToText, TTSettings  # Grammar Correction model
from gtts import gTTS  # Text-to-Speech library
import pyttsx3  # Text-to-Speech library
from google.colab import files  # File management library

# Initialize the Audio-to-Text model
model = WhisperModel("tiny")

# Function to transcribe audio and return the recognized text
def out(audio_file):
    segments, info = model.transcribe(audio_file)
    for segment in segments:
        x = segment.text
        return x

# Function to convert text to speech and save it as an audio file
def convert_text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

# Initialize the Grammar Correction model
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

# Function to convert audio to speech with grammar correction
def convert_audio_to_speech(input_audio_file, output_audio_file):
    # Step 1: Get the audio and transcribe it to text
    recognized_text = out(input_audio_file)
    recognized_text = recognized_text.lower()
    print(recognized_text)

    # Step 2: Apply grammar correction to the recognized text
    result = happy_tt.generate_text(recognized_text, args=args)
    print(result.text)

    # Step 3: Convert the corrected text to speech
    convert_text_to_speech(result.text, output_audio_file)

    # Step 4: Download the output audio file
    files.download(output_audio_file)
