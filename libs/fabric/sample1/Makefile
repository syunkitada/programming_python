env:
	sudo -E docker-compose up -d
	test -e venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

clean:
	sudo docker-compose down
