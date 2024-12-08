## Transcription (speech-to-text) microservice

### Setup for local development
1. Download and install FFmpeg:
    [ffmpeg.org](https://ffmpeg.org/download.html)
    * `ffmpeg -version`

3. Create a virtual environment:
    * `python -m venv venv-transcription`

4. Activate the environment:
    * `venv-transcription\Scripts\activate` (Windows); `source venv-transcription/bin/activate` (Ubuntu)

4. Install dependencies:
    * `pip install -r requirements.txt`
    * For ubuntu, also run `sudo apt-get install libportaudio2`

5. Install Whisper:
    * `pip install git+https://github.com/openai/whisper.git`

5. Run:
    * `uvicorn main:app --reload --port 8007`