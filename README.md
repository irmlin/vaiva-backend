# vaiva-backend


### Setup
1. Install python3.11 - [windows](https://www.python.org/downloads/release/python-3110/) link, [ubuntu](https://www.makeuseof.com/install-python-ubuntu/)  link
2. Create a virtual environment (venv):
   * `python3.11 -m venv venv`
   * Activate the environment - `venv\Scripts\activate` (windows); `source venv/bin/activate` (ubuntu)
   * In Pycharm IDE (if used), also activate the environment in the IDE: `file` -> `settings` -> `Project: vaiva-backend` -> `Add Interpreter` -> `Add Local Interpreter` -> `Existing` -> select path to created `venv` -> `ok` -> `apply` -> `ok`
3. Install packages - `pip install -r requirements.txt`


### Run the microservices
1. `python main-app/main.py` - API
2. `python video-avatar-microservice/main.py` - microservice for generating avatar videos