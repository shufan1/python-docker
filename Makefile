install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt



lint:
	pylint --disable=R,C app/main.py

format:
	black *.py

	
all: install lint test