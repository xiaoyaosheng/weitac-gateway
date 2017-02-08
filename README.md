# README #

get the healthy info of instance of marathon and user's order of stop/delete app for billing usage.

## weitac-gateway deployment

### install dependency

	sudo apt-get update
	sudo apt-get install -y git python-pip python-dev build-essential python-psycopg2
	git clone http://weitac-gateway.git
	cd weitac-gateway
	sudo pip install -r requirements.txt
	sudo mkdir /var/log/mathilde/
	sudo chown ubuntu:ubuntu /var/log/mathilde/

### modify settings.py(for production)

modify DATABASES settings

### migrate database

sudo python manage.py migrate

### test
	cd /home/ubuntu/weitac-gateway/test
	python event_tests.py


### subscribe eventbus from marathon

	
	docker run -d -p 8080:8080 --name weitac-gatway weitac-gatway