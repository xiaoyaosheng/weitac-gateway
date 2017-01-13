FROM docker.io/centos:7.2.1511
MAINTAINER "wangtengyu" <wang_tengyu@weitac.com>

ENV TERM xterm
ENV TZ "Asia/Shanghai"
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN yum -y install python-pip
RUN yum -y install epel-release python-pip libpq-dev python-devel nginx dnsutils mysql-devel gcc
RUN mkdir -p /var/log/weitac_gateway/ && \
    chmod 775 /var/log/weitac_gateway/

RUN pip install --upgrade pip
RUN easy_install supervisor
RUN pip install supervisor-stdout
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

RUN ln -s /weitac_gateway/conf/weitac_gateway_nginx.conf /etc/nginx/weitac_gateway_nginx.conf
RUN ln -s /weitac_gateway/conf/supervisord.conf /etc/supervisord.conf
RUN chmod +x /weitac_gateway/run.sh
CMD ["/usr/sbin/init"]
#CMD ["/weitac_gateway/run.sh"]