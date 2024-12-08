from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import sounddevice as sd
import numpy as np
import wave
import whisper
from pydub import AudioSegment
from io import BytesIO
import ffmpeg
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Initialize Whisper model
model = whisper.load_model("base")


@app.get("/")
def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Working:)"}


@app.post("/record")
def record_audio(filename: str = "audio.wav", duration: int = 10, samplerate: int = 44100):
    """
    Record audio and save it as a WAV file.
    """
    try:
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)


        print("Recording...")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype=np.int16)
        sd.wait()
        print("Recording complete.")

        # Save the audio to a WAV file
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)  # 2 bytes per sample for 16-bit audio
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())

        return {"message": f"Audio recorded and saved as {file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def convert_to_wav(file: UploadFile) -> BytesIO:
    """
    Convert an input file to WAV format if it is not already a WAV file.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        BytesIO: The converted WAV file in memory.
    """
    try:
        file_extension = file.filename.split(".")[-1].lower()
        file_data = BytesIO(file.file.read())

        if file_extension != "wav":
            # Convert to WAV
            audio = AudioSegment.from_file(file_data, format=file_extension)
            wav_data = BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
            return wav_data
        else:
            file_data.seek(0)
            return file_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to convert file to WAV: {e}")


def transcribe_wav(wav_data: BytesIO) -> str:
    """
    Transcribe a WAV audio file using the Whisper model.

    Args:
        wav_data (BytesIO): The WAV file in memory.

    Returns:
        str: Transcription of the audio.
    """
    try:
        # Decode BytesIO object into NumPy
        wav_data.seek(0)
        out, _ = (
            ffmpeg.input("pipe:0")
            .output("pipe:1", format="wav", ac=1, ar="16000")  # Convert to mono, 16 kHz
            .run(input=wav_data.read(), capture_stdout=True, capture_stderr=True)
        )

        # Load decoded audio into a NumPy array
        audio = np.frombuffer(out, dtype=np.int16).astype(np.float32)

        # Normalize audio to range [-1.0, 1.0]
        if np.max(np.abs(audio)) == 0:
            raise HTTPException(status_code=400, detail="Uploaded audio contains silence.")
        audio = audio / np.max(np.abs(audio))

        # Transcribe the audio
        result = model.transcribe(audio)

        if 'text' in result and result['text'].strip():
            return result['text']
        else:
            return "No transcription detected or transcription failed."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")



@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Accept an uploaded audio/video file, convert to WAV if necessary, and transcribe it using Whisper.
    """
    try:
        # Convert the uploaded file to WAV format if necessary
        wav_data = convert_to_wav(file)

        # Transcribe the WAV file
        transcription = transcribe_wav(wav_data)

        return {"filename": file.filename, "transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")



if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8007, log_level="info", reload=False)