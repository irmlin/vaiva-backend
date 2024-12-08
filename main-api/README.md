# vaiva-backend


### Setup (for local development)
1. Install python3.11 - [windows](https://www.python.org/downloads/release/python-3110/) link, [ubuntu](https://www.makeuseof.com/install-python-ubuntu/)  link
2. Open `main-api` as a project in pycharm
3. Create a virtual environment (venv):
   * `python3.11 -m venv venv-api`
   * Activate the environment - `venv-api\Scripts\activate` (windows); `source venv-api/bin/activate` (ubuntu)
   * In Pycharm IDE (if used), also activate the environment in the IDE: `file` -> `settings` -> `Project: main-app` -> `Add Interpreter` -> `Add Local Interpreter` -> `Existing` -> select path to created `venv-api` -> `ok` -> `apply` -> `ok`
4. Install packages - `pip install -r requirements.txt`
5. Run with `python main.py`

### Docker setup
1. Build docker image: `docker build -t main-api .`
2. Use `docker-compose.yml` file in project's root directory to run the container.



### Port:microservice map
1. `8001` : main-api
2. `8006` : chatbot-microservice
3. `8002` : voice-cloning (text-to-speech)
4. `8007` : speech-to-text
5. `8003` : image+audio to video (avatar video)


## Before having a conversation, do:

### Add features for LLM
1. Call http://localhost:8001/extract-features-for-persona-from-audio for saving features from audio
2. Call http://localhost:8001/extract-features-for-persona-from-text for saving features form text

All features are saved in `chatbot-microservice/src/data/features/<username>.txt`


### Add voice recording for voice-clone model
1. Client call to http://localhost:8001/files/upload-audio-for-voice (this call is done from frontend)
   * Call this endpoint to save an audio file for voice-clone model. Input - audio file and username.
   * The audio file is saved in `main-api/static/audio_for_voice/<username>.mp3/wav`. Is is always used when chatting with `username` clone.


## Order of endpoints that need to be called for conversation
1. Client call to http://localhost:8001/conversation with user message as input (this call is done from frontend)
   * From here, microservices are called one after another to generate response (this is done automatically)
       * If user message was text, http://localhost:8007/transcribe is called to get speech-to-text response 
       * Received text is used to call http://localhost:8006/send-message and return LLM text response
       * LLM text response is used to call http://localhost:8002/clone-voice and return text-to-speech result
2. Response is `{'llm_response': llm_response, 'audio_response_file': audio_response_title}`. From here:
   * Use `llm_response` to show text in chat window in frontend
   * For audio file (clone says the response in voice), call endpoint `http://localhost:8001/files/download-audio-response/{audio_response_title}`. Play the audio recording in frontend.