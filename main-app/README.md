# vaiva-backend


### Setup
1. Install python3.11 - [windows](https://www.python.org/downloads/release/python-3110/) link, [ubuntu](https://www.makeuseof.com/install-python-ubuntu/)  link
2. Open `main-app` as a project in pycharm
3. Create a virtual environment (venv):
   * `python3.11 -m venv venv-api`
   * Activate the environment - `venv-api\Scripts\activate` (windows); `source venv-api/bin/activate` (ubuntu)
   * In Pycharm IDE (if used), also activate the environment in the IDE: `file` -> `settings` -> `Project: main-app` -> `Add Interpreter` -> `Add Local Interpreter` -> `Existing` -> select path to created `venv-api` -> `ok` -> `apply` -> `ok`
4. Install packages - `pip install -r requirements.txt`


### Run API
1. `python main.py`
