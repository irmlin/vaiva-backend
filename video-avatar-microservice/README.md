# vaiva-backend

Sadtalker: https://github.com/OpenTalker/SadTalker

### Setup (for local development)
1. Install python3.8 - [windows](https://www.python.org/downloads/release/python-3110/) link, [ubuntu](https://www.makeuseof.com/install-python-ubuntu/)  link
2. Open `video-avatar-microservice` as a project in pycharm
3. Create a virtual environment (venv):
   * `python3.8 -m venv venv-avatar`
   * Activate the environment - `venv-avatar\Scripts\activate` (windows); `source venv-avatar/bin/activate` (ubuntu)
   * In Pycharm IDE (if used), also activate the environment in the IDE: `file` -> `settings` -> `Project: video-avatar-microservice` -> `Add Interpreter` -> `Add Local Interpreter` -> `Existing` -> select path to created `venv-avatar` -> `ok` -> `apply` -> `ok`
4. Install packages - `pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu113`
5. Download models:
   * Ubuntu
      * `cd src/external/sadtalker`
      * `bash scripts/download_models.sh`
   * Windows
     * Download from [here](https://github.com/OpenTalker/SadTalker?tab=readme-ov-file#pre-trained-models).
   * After downloading, you should have models in `src/external/sadtalker/checkpoints` and `src/external/sadtalker/gfpgan` folders
6. Run with `python main.py`

### Docker setup
1. Download models:
   * Ubuntu
      * `cd src/external/sadtalker`
      * `bash scripts/download_models.sh`
   * Windows
     * Download from [here](https://github.com/OpenTalker/SadTalker?tab=readme-ov-file#pre-trained-models).
   * After downloading, you should have models in `src/external/sadtalker/checkpoints` and `src/external/sadtalker/gfpgan` folders
2. Build docker image: `docker build -t video-avatar-microservice .`
3. Use `docker-compose.yml` file in project's root directory to run the container.
