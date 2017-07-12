

run:
	python run_app.py

deploy:
	cd ansible; ansible-playbook pi.yml -i hosts -v --ask-pass --vault-password-file=../venv/ansible.txt
