# vaiva-backend

## chatbot microservice

### setup for local development
1. download and install ollama:
    [github](https://github.com/ollama/ollama?tab=readme-ov-file#ollama)

2. pull llama3.2 3b model by running ollama:
    * `ollama run llama3.2`

3. create virtual environment:
    * `python -m venv venv-chat`
    * `venv-chat\Scripts\activate`

4. install required packages:
 * `pip install -r requirements.txt`

5. run with `python main.py` or `uvicorn main:app --reload --port 8006`
