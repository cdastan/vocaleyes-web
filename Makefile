.PHONY: help

help:
	@echo
	@echo "USAGE: make [target]"
	@echo
	@echo "TARGETS:"
	@echo
	@echo "  install    - create virtual env, etc"
	@echo "  deploy     - deploy app
	@echo "    start    - start application"
	@echo "     test    - run tests"""
	@echo

install:
	@bash script/install.sh

deploy:
	@bash script/deploy.sh

start:
	@venv/bin/python app/server.py --logging=debug

test:
	@nosetests app/test --nologcapture

