OS = Linux

VERSION = 0.0.1

CURDIR = $(shell pwd)
SOURCEDIR = $(CURDIR)

ECHO = echo
RM = rm -rf
MKDIR = mkdir
FLAKE8 = flake8
PIP_INSTALL = pip install
RUN_MOCK_TESTS = ./run-mock-tests.sh

.PHONY: setup build test help

all: setup build test

setup:
	$(PIP_INSTALL) $(FLAKE8)

build:
	$(FLAKE8) $(SOURCEDIR) --show-source --show-pep8 --statistics --count

test:
	$(RUN_MOCK_TESTS)

help:
	@$(ECHO) "Targets:"
	@$(ECHO) "all     - setup, build and test"
	@$(ECHO) "setup   - set up prerequisites for build"
	@$(ECHO) "build   - perform static analysis"
	@$(ECHO) "test    - run unit tests"