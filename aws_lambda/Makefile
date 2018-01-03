SCRIPT_DIR=$(realpath $(shell dirname $(lastword $(MAKEFILE_LIST))))
LAMBDA_S3_PATH ?= s3://alexa-automation/lambdas
STAGE ?= prod

.PHONY: build deploy

build:
	echo "Make Lambda packages for ${STAGE}"
	sh bin/build.sh ${STAGE}

deploy:
	echo "Script dir: $(SCRIPT_DIR)"
	if [ ! -d "$(SCRIPT_DIR)/dist" ]; then \
		echo "Packages not found. Please build them first"; \
		exit 1; \
	fi
	echo "Deploying"
	aws s3 cp dist/ $(LAMBDA_S3_PATH)/ --recursive --include "*.zip"
