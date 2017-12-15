SCRIPT_DIR=$(realpath $(shell dirname $(lastword $(MAKEFILE_LIST))))
PROJECT_ROOT=$(realpath $(shell dirname $(lastword $(MAKEFILE_LIST)))/../)


run:
	python run_app.py > /tmp/smarty.log 2>&1 &

deploy:
	cd ansible; ansible-playbook pi.yml -i hosts -v --ask-pass --vault-password-file=../venv/ansible.txt

stop:
	ps -ef | grep "run_app.py" | grep -v grep | awk '{print $$2}' | xargs -I ARGS kill ARGS

test: stop run
	echo