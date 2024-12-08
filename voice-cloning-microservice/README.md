For a local run, `python -m unidic download`

# How to run (docker)
Download the checkpoint from [here](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip) and extract it to the `checkpoints_v2` folder. `src/checkpoints_v2/converter/*` and `src/checkpoints_v2/base_speakers` should exist
docker build -t voice-cloning .
docker run -it --gpus all -p 8002:8002 --name voice-cloning -v ./src/outputs:/app/src/outputs/ -v ./src/inputs:/app/src/inputs/ -v ./src/processed:/app/src/processed/ voice-cloning

Change int8 into float16 in se_extractor if your pc supports float16
