import sounddevice as sd
import vosk
import json
import queue

def listen_and_convert_to_text():
    model_path = 'models/vosk-model-small-en-us-0.15'
    vosk_model = vosk.Model(model_path)

    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(f"SoundDevice status: {status}")
        q.put(bytes(indata))

    # Use the default input device parameters
    samplerate = int(sd.query_devices(kind='input')['default_samplerate'])
    channels = 1

    # Start the audio stream and process the data
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                               channels=channels, callback=callback):
            print("Please say something...")
            sd.sleep(5000)  # Record for 5 seconds

            # Collect all recorded data
            audio_data = b''.join(list(q.queue))

            # Initialize the recognizer
            recognizer = vosk.KaldiRecognizer(vosk_model, samplerate)

            # Process the accumulated audio data
            if recognizer.AcceptWaveform(audio_data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print(f"You said: {text}")
                return text
            else:
                print("Sorry, could not process the audio.")
                return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    text_output = listen_and_convert_to_text()
