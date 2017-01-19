FROM ubuntu:16.04
MAINTAINER wangtengyu wang_tengyu@weitac.com

RUN apt-get update && \
    apt-get install -y libpq-dev python-pip python-dev nginx dnsutils libmysqlclient-dev rabbitmq-server && \
    mkdir -p /var/log/weitac-gateway/ && \
    chmod 775 /var/log/weitac-gateway/

RUN easy_install supervisor
RUN easy_install supervisor-stdout 
RUN pip install uwsgi
RUN rm -rf /etc/nginx/sites-enabled/default

# nginx config
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir -p /var/log/weitac-gateway
RUN mkdir -p /var/log/uwsgi/

WORKDIR /weitac-gateway
ENV C_FORCE_ROOT="true"
EXPOSE 8080

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /weitac-gateway

RUN ln -s /weitac-gateway/conf/weitac-gateway_nginx.conf /etc/nginx/sites-enabled/weitac-gateway_nginx.conf
RUN ln -s /weitac-gateway/conf/supervisord.conf /etc/supervisord.conf
RUN chmod +x /weitac-gateway/run.sh

CMD ["/weitac-gateway/run.sh"]
