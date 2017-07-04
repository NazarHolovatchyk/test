# Alexa REST service

## Setup

    cd svc
    virtualenv venv
    pip install -r requirements.txt
    
### Raspberry
    
    sudo apt-get install -y supervisor nginx
    sudo rm /etc/nginx/sites-enabled/default
    sudo cp ops/supervisor-app.conf /etc/supervisor/conf.d/
    sudo cp ops/nginx-app.conf /etc/nginx/sites-enabled/
