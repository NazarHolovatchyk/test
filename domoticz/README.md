# Setup

## Device list

192.168.1.200 - domoticz
192.168.1.201 (B4:43:0D:FB:C9:F5) - RM PRO


## Shell setup

	ssh pi@domoticz.local
	cd ~
	sh domoticz/scripts/disk_space.sh
	source ~/domoticz/venv/bin/activate
	
	# LG TV ON
	/home/pi/domoticz/venv/bin/python /home/pi/domoticz/scripts/python/broadlink_cli.py rm -i 192.168.1.201 -m B4:43:0D:FB:C9:F5 -c JgBIAAABJpMTEhMREzcTERMSExETEhMREzcTNhMREzcSNxM2EzYTNhMSExETEhM2ExITERMSExITNhM2EzYTEhM2EzYTNhM2EwANBQ==
	scripts://python/broadlink_cli.py rm -i 192.168.1.201 -m B4:43:0D:FB:C9:F5 -c JgCQAAABFooTMhIREjISERIRETQSEBIzExARNBIQEjQRMxMQEzIREhIQEhESMxE0Ew8SERIzERISMhMzERESERMyETQSEBIzEgADgQABFYsSNBASEjMRERIRETQSEREzExEQNBMQETQRNBEREjQQEhIRERETMhE0EhERERI0EBISMxE0EhERERMyETQSEREzEwANBQAAAAAAAAAA

## UI setup

In Domoticz create dummy `hardware`. On `Switches` tab add new switch based on dummy hardware. Press `Edit` and populate `On/Off Action` field with:

	script://python/broadlink_cli.py rm -i 192.168.1.201 -m B4:43:0D:FB:C9:F5 -c JgBIAAABJpMTEhMREzcTERMSExETEhMREzcTNhMREzcSNxM2EzYTNhMSExETEhM2ExITERMSExITNhM2EzYTEhM2EzYTNhM2EwANBQ==
	
