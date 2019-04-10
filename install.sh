#!/bin/bash
if [ "$UID" != "0" ]; then
echo "Please run this script by root "
exit 1
#intsll yum package
yum -y update
yum install -y yum-utils
yum groupinstall -y development
yum install -y https://centos7.iuscommunity.org/ius-release.rpm

#python3.6 pip devel

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
#restart server

#start process
#configure Nginx
vim /usr/lib/systemd/system/nginx.servcie

#nginx服务配置到该文件中
#服务描述性的配置
[Unit]
Description=nginx - high performance web server
Documentation=http://nginx.org/en/docs/
After=network.target remote-fs.target nss-lookup.target
#服务关键配置
[Service]
Type=forking
#pid文件位置 
#要与nginx配置文件中的pid配置路径一致，这个很重要，否则会服务启动失败
PIDFile=/var/run/nginx.pid
#启动前检测 nginx配置文件 是否正确
ExecStartPre=/usr/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
#启动
ExecStart=/usr/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
#重启
ExecReload=/bin/kill -s HUP $MAINPID
#关闭
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true
[Install]
WantedBy=multi-user.target

systemctl start nginx.service
systemctl enable nginx.service

uwsgi --http :8001 --chdir /root/easy_cmdb/  --wsgi-file easy_cmdb/wsgi.py 
#--static-map /static=/root/easy_cmdb/statci
#--check-static /root/easy_cmdb/statci

#管理 supervisor
echo_supervisord_conf > /etc/supervisord.conf
vim
[program:ecmdb]
command=/path/to/uwsgi --http :8001 --chdir /root/easy_cmdb/  --wsgi-file easy_cmdb/wsgi.py 
directory=/path/to/zqxt
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true




