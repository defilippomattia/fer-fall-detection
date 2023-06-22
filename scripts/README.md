# Scripts 
Fall detection scripts, pager app and simulating POST request


Prerequisites:  
Python 3.10.0 (mediapipe is not compatible with Python 3.11.0)  
pip 21.2.3  

`python -m venv venv` (optional)  
`./venv/Scripts/activate` (optional)  
`pip install -r requirements.txt`  


## Fall detection
Starting fall detection script.  
`cd fer-fall-detect/scripts`  
`python detect_fall_clean.py`


## Pager app
Startign simulated pager app.

`cd fer-fall-detect/scripts/simulations/pager`   
`python app.py`

## Simulating POST request

Simulating falls with POST requests.  
`cd fer-fall-detect/scripts/simulations`  
`python sim_watch_notebook.py`  
`python sim_watch.py`  
`python notebook.py`   



