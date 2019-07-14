#!/bin/sh
sudo su
yum install update -y
yum install docker -y
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
service docker start
usermod -aG docker ec2-user
yum install git -y
mkdir app && cd app/
git clone https://github.com/TyLeRRR/aws-the-right-way
cd aws-the-right-way/static-webhosting/
docker-compose up -d