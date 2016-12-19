FROM ubuntu:trusty
MAINTAINER ruicao ruicao@mathildetech.com

RUN apt-get update && \
    apt-get install -y libpq-dev python-pip python-dev nginx dnsutils && \
    mkdir -p /var/log/mathilde/ && \
    chmod 775 /var/log/mathilde/

RUN easy_install supervisor
RUN easy_install supervisor-stdout 
RUN pip install uwsgi
RUN rm -rf /etc/nginx/sites-enabled/default

# nginx config
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir -p /var/log/mathilde
RUN mkdir -p /var/log/uwsgi/

WORKDIR /slark

EXPOSE 8080

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /slark

RUN ln -s /slark/conf/slark_nginx.conf /etc/nginx/sites-enabled/slark_nginx.conf
RUN ln -s /slark/conf/supervisord.conf /etc/supervisord.conf
RUN chmod +x /slark/run.sh

CMD ["/slark/run.sh"]
