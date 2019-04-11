#!/bin/bash
if [ "$UID" != "0" ]; then
echo "Please run this script by root "
exit 1
#_________intsll yum package_____________
yum -y update
yum install -y yum-utils
yum groupinstall -y development
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
#_________intsll python3.6 pip devel_____________

yum install -y vim python36u python36u-pip python36u-devel mariadb mariadb-server
 
#upgrade pip
python3.6 -m pip install --upgrade pip

#django version 2.0.5
python3.6 -m pip install django==2.0.5

#ansible version2.7.1
python3.6 -m pip install ansible==2.7.1

#PyMySQL version 0.9.2
python3.6 -m pip install PyMySQL==0.9.2
#bs4 version 0.0.1
python3.6 -m pip install bs4==0.0.1
#xlrd version 1.2.0
python3.6 -m pip install xlrd==1.2.0
#xlwt version 1.3.0
python3.6 -m pip install xlwt==1.3.0
#requests version 2.18.4
python3.6 -m pip install requests==2.18.4
#selenium version 3.141.0
python3.6 -m pip install selenium==3.141.0
#mariadb version 10.1.38
#yum list | grep mariadb
systemctl start mariadb
systemctl enable mariadb

#msyql_secure_installation set password
#mysql -u root -p  testlogin
#create database
touch scheme.sql
echo "create user cmdbadmin;" >> scheme.sql
echo "create database easy_cmdb character set = utf8;" >> scheme.sql
echo "grant all on easy_cmdb.* to 'cmdbadmin'@'%' identified by '123456';" >> scheme.sql
echo "grant all on easy_cmdb.* to 'cmdbadmin'@'localhost' identified by '123456';" >> scheme.sql
echo "flush privileges;" >> scheme.sql
mysql -u root < scheme.sql 

#install supervisor manage process tools
python3.6 -m pip install supervisor
#install nginx
yum install -y nginx

#close SELinux
setenforce 0

#close firewall
systemctl stop firewalld
#open the port
#firewall-cmd --zone=public --add-port=80/tcp --permanent
#firewall-cmd --reload

#before uwsgi  install pcre ENV
#python3.6 -m pip uninstall uwsgi 
yum install -y pcre pcre-devel pcre-static
python3.6 -m pip install uwsgi --upgrade


#download code
yum install -y git
#use low copy ,copy the last version
git clone --depth=1 https://github.com/chry1988/easy_cmdb.git
#git@github.com:chry1988/easy_cmdb.git

#data migrations 
cd easy_cmdb
python3.6 manage.py makemigrations
python3.6 manage.py migrate
#--------------------------------------------------------------------------------
#configure uwsgi
#uwsgi --http :8001 --chdir /root/easy_cmdb/easy_cmdb  --module wsgi.py
uwsgi --http :8001 --chdir /root/easy_cmdb/  --wsgi-file easy_cmdb/wsgi.py

uwsgi --http :8001 --chdir /root/easy_cmdb/  --wsgi-file easy_cmdb/wsgi.py 
#--static-map /static=/root/easy_cmdb/statci
#--check-static /root/easy_cmdb/statci

#_________configure web server uwsgi_____________
# uwsgi --http :8001 --chdir /root/easy_cmdb/  --wsgi-file easy_cmdb/wsgi.py

mkdir /root/easy_cmdb/
touch /root/easy_cmdb/uwsgi.ini

#__________the document in uwsgi.ini____________

[uwsgi]
#socket = /root/easy_cmdb/easy_cmdb.sock
http = 172.20.51.160:8001
chdir = /root/easy_cmdb/
wsgi-file = easy_cmdb/wsgi.py
touch-reload = /root/easy_cmdb/reload
static-map = /static=/root/easy_cmdb/static
processes = 2
threads = 4

chmod-socket = 664
#chown-socket = root:www-data
uid = root
gid = root
vacuum = true

#___________end of uwsgi.ini__________

#___________teset ini file____________
uwsgi --ini uwsgi.ini
#_________configure supervisord_________________
echo_supervisord_conf > /etc/supervisord.conf

echo "[program:easy_cmdb]" >> etc/supervisord.conf
#command=/bin/uwsgi --http :8001 --chdir /root/easy_cmdb/  --wsgi-file easy_cmdb/wsgi.py
echo "command=/bin/uwsgi --ini /root/easy_cmdb/uwsgi.ini" >> etc/supervisord.conf
echo "directory=/root/easy_cmdb" >> etc/supervisord.conf
echo "startsecs=0" >> etc/supervisord.conf
echo "stopwaitsecs=0" >> etc/supervisord.conf
echo "autostart=true" >> etc/supervisord.conf
echo "autorestart=true" >> etc/supervisord.conf

#________operate to supervisord___________
#supervisord -c /etc/supervisord.conf
#supervisorctl -c /etc/supervisord.conf restart easy_cmdb
#supervisorctl -c /etc/supervisord.conf [start|stop|restart] [program-name|all]

#_________the part of nginx is not finished________

mkdir /etc/nginx/sites-available/
touch easy_cmdb.conf
vim /etc/nginx/sites-available/easy_cmdb.conf

# the upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
#----------------------
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name easy_cmdb.com; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media/  {
        alias /root/easy_cmdb/media;  # your Django project's media files - amend as required
    }

    location /static/ {
        alias /root/easy_cmdb/static/; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  unix:///root/easy_cmdb/easy_cmdb.sock;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
}
#---
#user root
/etc/nginx/nginx.conf
include /etc/nginx/sites-enabled/*.conf;
ln -s ~/path/to/your/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/easy_cmdb.conf /etc/nginx/sites-enabled/
#change the default configure

service nginx reload

#start process
#configure Nginx
vim /usr/lib/systemd/system/nginx.servcie

#nginx�������õ����ļ���
#���������Ե�����
[Unit]
Description=nginx - high performance web server
Documentation=http://nginx.org/en/docs/
After=network.target remote-fs.target nss-lookup.target
#����ؼ�����
[Service]
Type=forking
#pid�ļ�λ��
#Ҫ��nginx�����ļ��е�pid����·��һ�£��������Ҫ��������������ʧ��
PIDFile=/var/run/nginx.pid
#����ǰ��� nginx�����ļ� �Ƿ���ȷ
ExecStartPre=/usr/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
#����
ExecStart=/usr/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
#����
ExecReload=/bin/kill -s HUP $MAINPID
#�ر�
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true
[Install]
WantedBy=multi-user.target

systemctl start nginx.service
systemctl enable nginx.service

