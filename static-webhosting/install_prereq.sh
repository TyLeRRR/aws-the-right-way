#!/bin/sh
yum update -y
yum install httpd -y
service httpd start
chkconfig httpd on
aws s3 cp s3://aws-the-right-way/ec2-webpage/index.html /var/www/html
aws s3 cp s3://aws-the-right-way/ec2-webpage/error.html /var/www/error