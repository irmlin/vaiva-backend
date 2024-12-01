python -m unidic download

# How to run
docker build -t voice-cloning .
docker run -it --gpus all -p 8002:8002 voice-cloning

Change int8 into float16 in se_extractor if your pc supports float16
