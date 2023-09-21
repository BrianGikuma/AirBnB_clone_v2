#!/usr/bin/env bash
# prepares a server for deployment

FAKE_CONTENT="<html>
<head>
</head>
<body>
Holberton School
</body>
</html>
"

sudo apt update -y
sudo apt install -y nginx

test -d /data/web_static/releases/test/ || sudo mkdir -p /data/web_static/releases/test/
test  -d /data/web_static/shared/ || sudo mkdir -p /data/web_static/shared
test -f /data/web_static/releases/test/indext.html || sudo touch /data/web_static/releases/test/index.html
echo -e "$FAKE_CONTENT" | sudo tee /data/web_static/releases/test/index.html
sudo ln -fs /data/web_static/releases/test/ /data/web_static/current

sudo chown --recursive ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server;/a\\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-enabled/default

sudo service nginx restart
