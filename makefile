.PHONY: init
init:
	pip3 install -r requirements.txt

.PHONY: test
test:
	python3 -m unittest discover

.PHONY: run
run:
	python3 application/querio.py

.PHONY: run-test
run-test:
	python3 application/querio.py -- --run-test

.PHONY: build
build:
	pyinstaller -y --clean querio.spec

.PHONY: run_build
run_build:
	./dist/querio/querio

.PHONY: run_build-test
run_build-test:
	./dist/querio/querio -- --run-test
