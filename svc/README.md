# Alexa REST service

## Setup

    cd svc
    virtualenv venv
    pip install -r requirements.txt
    
### Raspberry
    
    sudo apt-get install -y supervisor
    cp supervisor_app.conf /etc/supervisor/conf.d/