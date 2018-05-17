#!/usr/bin/python

import os
import subprocess
import glob
import shutil

args = os.environ.copy()

def recursive_copy_files(source_path, destination_path, override=False):
    """
    Recursive copies files from source  to destination directory.
    :param source_path: source directory
    :param destination_path: destination directory
    :param override if True all files will be overridden otherwise skip if file exist
    :return: count of copied files
    """
    files_count = 0
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    items = glob.glob(source_path + '/*')
    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            if not os.path.exists(file) or override:
                shutil.copyfile(item, file)
                files_count += 1
    return files_count

#copy default nginx confg
files_copied = recursive_copy_files("/conf/default_config/","/etc/nginx/")
print(files_copied)

# Check if a stale pid file exists
if os.path.exists("/var/log/nginx.pid"):
    os.remove("/var/log/nginx.pid")

if 'TLS_FLAVOR' not in locals()['args']:
    print("TLS_FLAVOR not set. Falling back to none.")
    os.environ['TLS_FLAVOR'] = 'notls'

#start certbot listener
if os.environ["TLS_FLAVOR"] in [ "letsencrypt" ]:
    print("TLS_FLAVOR set to {}".format(os.environ["TLS_FLAVOR"]))
    subprocess.Popen(["/usr/bin/python","/letsencrypt.py"])

subprocess.call(["/usr/bin/python","/config.py"])
os.execv("/usr/sbin/nginx", ["nginx", "-g", "daemon off;"])
