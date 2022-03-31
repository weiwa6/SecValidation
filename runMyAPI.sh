#!/usr/bin/env bash

cd /home/ubuntu/SecValidation/
source /home/ubuntu/SecValidation/venv/bin/activate
python /home/ubuntu/SecValidation/app.py >> /home/ubuntu/runMyAPI.log 2>&1
## DO SOME STUFF -> USE FULL PATH HERE TOO #
deactivate
