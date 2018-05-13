FROM alpine:edge

RUN apk add --no-cache nginx nginx-mod-mail python py-jinja2 certbot openssl

COPY conf /conf
COPY *.py /

EXPOSE 80/tcp 443/tcp

CMD /start.py
