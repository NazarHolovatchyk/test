sudo crontab -e
# 0 30 21 * * ? /home/pi/smarty/venv/bin/python /home/pi/smarty/svc/cli.py -d door -c off
# 0 30 8 * * ? /home/pi/smarty/venv/bin/python /home/pi/smarty/svc/cli.py -d door -c on
