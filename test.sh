sudo apt-get update -y && sudo apt-get install -y docker docker-compose && git clone https://github.com/defilippomattia/fer-fall-detection.git

sudo docker stop $(sudo docker ps -aq) && sudo docker rm $(sudo docker ps -aq) && sudo docker volume rm $(sudo docker volume ls -q)

sudo docker-compose build

 sudo docker-compose up --force-recreate -d