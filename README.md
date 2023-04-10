# fer-fall-detection

# Introduction
Repo for the master thesis "An alerting system based on fall detection of elderly people"

# How to start
Needs config.toml file which is currently not commited.

I'm using Python 3.10.0 and pip 21.2.3 (mediapipe is not compatible with 3.11.0).

## Windows

`git clone https://github.com/defilippomattia/fer-fall-detect`  
`cd fer-fall-detect`  
`pip install -r requirements.txt`   
`python app.py`  
`python detect_fall.py`  

## Linux
todo...



`git clone https://github.com/defilippomattia/fer-fall-detect`  
`cd fer-fall-detect`  
OPTIONAL:
`python -m venv venv`
`./venv/Scripts/activate`
`docker-compose up --force-recreate`
`pip install -r requirements.txt`
`cd fer-fall-detect/backend`  
`go mod tidy`
`go run server.go`
`cd fer-fall-detect/frontend`  
`npm install`
`npm run dev`


