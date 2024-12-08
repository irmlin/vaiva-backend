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

### Order of endpoints to be called 
1. Client call to http://localhost:8001/conversation with user message as input
   * If user message was text, call http://localhost:8007/transcribe to get speech-to-text response 
2. Use received text to call http://localhost:8006/send-message and return LLM text response
3. Use LLM text response to call http://localhost:8002/clone-voice and return text-to-speech result