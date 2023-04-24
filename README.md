# fer-fall-detection

# Introduction
Repo for the master thesis "An alerting system based on fall detection of elderly people"

# How to start

Python 3.10.0 (mediapipe is not compatible with Python 3.11.0)  
pip 21.2.3  
go 1.20.1

## Set environment variables

### Windows
Run as admin (from powershell for eg.): fer-fall-detect/scripts/setenvvar/win.ps1
### Linux



`git clone https://github.com/defilippomattia/fer-fall-detect`  
`cd ./fer-fall-detect`  
`python -m venv venv` (optional)  
`./venv/Scripts/activate` (optional)  
`pip install -r requirements.txt`  
`docker-compose up --force-recreate`

Start web server:  
`cd fer-fall-detect/backend`   
`go mod tidy`  
`go run server.go` 

Start frontend:  
`cd fer-fall-detect/frontend`   
`npm install`  
`npm run dev`

Visit http://localhost:6501 (frontend)  
Visit http://localhost:6503 (mongo gui)

Starting camera feed:  
`cd fer-fall-detect/scripts`  
`python detect_fall.py`

Simulating falls and subscribers:  
`cd fer-fall-detect/scripts/simulations`  
`python sim_watch_notebook.py`  
`python sim_subscriber_1.py`  






