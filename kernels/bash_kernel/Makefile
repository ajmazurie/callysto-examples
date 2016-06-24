
PROJECT_NAME := $(shell python setup.py --name)

SHELL := /bin/bash
BOLD := \033[1m
DIM := \033[2m
RESET := \033[0m

all: uninstall install clean

uninstall:
	@echo -e "$(BOLD)uninstalling '$(PROJECT_NAME)'$(RESET)"
	-@pip uninstall -y $(PROJECT_NAME) 2> /dev/null

install:
	@echo -e "$(BOLD)installing '$(PROJECT_NAME)'$(RESET)"
	@echo -e -n "$(DIM)"
	@pip install --process-dependency-links .
	@callysto-install-kernel $(PROJECT_NAME)
	@echo -e -n "$(RESET)"

clean:
	@echo -e "$(BOLD)cleaning '$(PROJECT_NAME)' repository$(RESET)"
	@rm -rf build
	@rm -rf dist
	@rm -rf **/$(PROJECT_NAME).egg-info
	@rm -rf $(PROJECT_NAME).egg-info
	@rm -rf .eggs
