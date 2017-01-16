# README #

get the healthy info of instance of marathon and user's order of stop/delete app for billing usage.

## weitac_gateway deployment

### install dependency

	sudo apt-get update
	sudo apt-get install -y git python-pip python-dev build-essential python-psycopg2
	git clone https://username@bitbucket.org/mathildetech/weitac_gateway.git
	cd weitac_gateway
	sudo pip install -r requirements.txt
	sudo mkdir /var/log/mathilde/
	sudo chown ubuntu:ubuntu /var/log/mathilde/

### modify settings.py(for production)

modify DATABASES settings

### migrate database

sudo python manage.py migrate

### test
	cd /home/ubuntu/weitac_gateway/test
	python event_tests.py

### add cron:

	@reboot /usr/bin/python /home/ubuntu/weitac_gateway/manage.py runserver 0.0.0.0:8080

### subscribe eventbus from marathon

	curl -X POST -H "Content-Type:application/json" -d '{}' https://marathon.alauda.club:8443/v2/eventSubscriptions?callbackUrl=https://weitac_gateway.alauda.club:8443/v1/instance/events/
	
	docker -d -p 8080:8080 weitac