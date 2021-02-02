FROM alpine:3.13.1

RUN apk add --no-cache nginx nginx-mod-mail python3 py3-jinja2 certbot openssl
RUN ln -s /usr/bin/python3 /usr/bin/python
COPY conf /conf
COPY *.py /

EXPOSE 80/tcp 443/tcp

CMD ["/start.py"]
