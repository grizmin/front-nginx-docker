#!/usr/bin/python

import jinja2
import os

convert = lambda src, dst, args: open(dst, "w").write(jinja2.Template(open(src).read()).render(**args))

args = os.environ.copy()

# Get the first DNS server
with open("/etc/resolv.conf") as handle:
    content = handle.read().split()
    args["RESOLVER"] = content[content.index("nameserver") + 1]

# TLS configuration
if 'TLS_FLAVOR' not in locals()['args']:
    args['TLS_FLAVOR'] = 'notls'

args["TLS"] = {
    "cert": ("/certs/cert.pem", "/certs/key.pem"),
    "letsencrypt": ("/certs/letsencrypt/live/front/fullchain.pem",
        "/certs/letsencrypt/live/front/privkey.pem"),
    "notls": None
}[args["TLS_FLAVOR"]]

if args["TLS"] and not all(os.path.exists(file_path) for file_path in args["TLS"]):
    print("Missing cert or key file, disabling TLS")
    args["TLS_ERROR"] = True

# Build final configuration paths
nginx_configs={
    '/conf/default_server.conf': '/etc/nginx/conf.d/default_server.conf',
    '/conf/tls.conf': "/etc/nginx/tls.conf",
    '/conf/proxy.conf': "/etc/nginx/proxy.conf",
    '/conf/nginx.conf': "/etc/nginx/nginx.conf"
}

for config_path in nginx_configs.items():
    convert(config_path[0], config_path[1], args)

if os.path.exists("/var/log/nginx.pid"):
    os.system("nginx -s reload")
