# Ansible deployment

    (env)$ cd ansible
    (env)$ ansible-playbook pi.yml -i hosts -v --ask-pass --ask-vault-pass
        
Push code updates only (Event Collector and LogStash):

    (env)$ ansible-playbook pi.yml -i hosts -v --ask-pass --ask-vault-pass --tags "push_updates"
