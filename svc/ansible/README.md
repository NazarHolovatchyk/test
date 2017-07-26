# Ansible deployment

    (env)$ cd ansible
    (env)$ ansible-playbook pi.yml -i hosts -v --ask-pass --ask-vault-pass
        
Push code updates only (Event Collector and LogStash):

    (env)$ ansible-playbook pi.yml -i hosts -v --ask-pass --ask-vault-pass --tags "push_updates"

SSL certificate configured from
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04

cert renew in cron

	15 3 * * * /usr/bin/certbot renew --quiet --renew-hook "/bin/systemctl reload nginx"
	