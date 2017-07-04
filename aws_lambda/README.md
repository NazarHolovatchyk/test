# AWS lambdas

AWS lambdas as backend of Alexa skills

## Setup

    pip install -r requirements.txt
    
## Alexa lambdas

    make lambda
    ls dist
    make deploy
    aws s3 ls s3://alexa-automation/lambdas
