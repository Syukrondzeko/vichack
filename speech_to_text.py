from fastapi import FastAPI, UploadFile, File, HTTPException
import vosk
import wave
import json
import os
from fastapi.responses import JSONResponse

app = FastAPI()

# Load the Vosk model once to avoid reloading it for each request
model_path = 'models/vosk-model-small-en-us-0.15'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model path '{model_path}' not found.")
vosk_model = vosk.Model(model_path)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    # Check if the uploaded file is a WAV file
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only WAV files are supported.")

    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Open the WAV file and process it
    try:
        with wave.open(temp_file_path, "rb") as wf:
            # Check if the WAV file has the expected format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != 'NONE':
                raise HTTPException(status_code=400, detail="Audio file must be WAV format mono PCM.")

            # Initialize the recognizer with the sample rate from the WAV file
            recognizer = vosk.KaldiRecognizer(vosk_model, wf.getframerate())

            # Read the audio data and process it
            while True:
                data = wf.readframes(4000)  # Read data in chunks
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)

            # Get the final result
            final_result = recognizer.FinalResult()
            text = json.loads(final_result).get("text", "")
            return JSONResponse(content={"recognized_text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
