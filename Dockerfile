FROM ubuntu:16.04
MAINTAINER wangtengyu wang_tengyu@weitac.com

RUN apt-get update && \
    apt-get install -y libpq-dev python-pip python-dev nginx dnsutils libmysqlclient-dev && \
    mkdir -p /var/log/weitac_gateway/ && \
    chmod 775 /var/log/weitac_gateway/

RUN easy_install supervisor
RUN easy_install supervisor-stdout 
RUN pip install uwsgi
RUN rm -rf /etc/nginx/sites-enabled/default

# nginx config
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir -p /var/log/weitac_gateway
RUN mkdir -p /var/log/uwsgi/

WORKDIR /weitac_gateway

EXPOSE 8080

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /weitac_gateway

RUN ln -s /weitac_gateway/conf/weitac_gateway_nginx.conf /etc/nginx/sites-enabled/weitac_gateway_nginx.conf
RUN ln -s /weitac_gateway/conf/supervisord.conf /etc/supervisord.conf
RUN chmod +x /weitac_gateway/run.sh

CMD ["/weitac_gateway/run.sh"]
