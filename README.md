# Amazon Web Services the Right Way

### Introduction

This project serves as the implementation of goals to grow from basic AWS knowledge to understanding and deploying complex architectures in an automated way.
The main goal is to find out and implement the "right way", not the quick way. We do the quick way first then refactor to the right way before moving on.
Shut down or de-provision as much as we can between learning sessions. Rebuilding often will reinforce concepts anyway.

### Project Overview

We use a simple website as an excuse to use all the technologies AWS puts at our fingertips. 

This guide takes us from the most basic webpage to an extremely cheap scalable web application.

*Stock-Symbol-of-the-Day* - Display a random stock symbol each page load, have a box at the bottom and a submit button to add a new symbol to the random symbol list.

#### Account Basics

- [x] Create an IAM user for personal use.
- [x] Set up MFA for the root user, turn off all root user API keys.
- [x] Set up Billing Alerts for anything over a few euros.
- [x] Configure the AWS CLI for our user using API credentials.

- [x] **Checkpoint:** We can use the AWS CLI to interrogate information about our AWS account.

#### Web Hosting Basics

- [ ] Deploy an EC2 VM and host a simple static *Stock-Symbol-of-the-Day Coming Soon* web page.
- [ ] Take a snapshot of our VM, delete the VM, and deploy a new one from the snapshot. Basically, disk backup + disk restore.

**Checkpoint:** We can view a simple HTML page served from our EC2 instance.

#### Auto Scaling

- [ ] Create an AMI from that VM and put it in an autoscaling group, so one VM always exists.
- [ ] Put an Elastic Load Balancer in front of that VM and load balance between two Availability Zones (one EC2 in each AZ).

**Checkpoint:** We can view a simple HTML page served from both of our EC2 instances. We can turn one off, and our website is still accessible.


#### External Data

- [ ] Create a DynamoDB table and experiment with loading and retrieving data manually, then do the same via a script on a local machine.
- [ ] Refactor static page into Stock-Symbol-of-the-Day website (JS, PHP, Python ... ) which reads/updates a list of symbols in the AWS DynamoDB table. (Hint: EC2 Instance Role)

**Checkpoint:** High-Available(HA)/AutoScaled website can now load/save data to a database between users and sessions.


#### Web Hosting Platform-as-a-Service

- [ ] Retire that simple website and re-deploy it on Elastic Beanstalk.
- [ ] Create a S3 Static Website Bucket, upload some sample static pages/files/images. Add those assets to our Elastic Beanstalk website.
- [ ] Register a domain (or re-use an existing one). 
- [ ] Set Route53 as the Nameservers and use Route53 for DNS. 
- [ ] Make www.ourdomain.com go to our Elastic Beanstalk. 
- [ ] Make static.ourdomain.com serve data from the S3 bucket.
- [ ] Enable SSL for our Static S3 Website. It isn't exactly trivial. (Hint: CloudFront + ACM)
- [ ] Enable SSL for our Elastic Beanstalk Website.

**Checkpoint:** HA/AutoScaled website now serves all data over HTTPS. The same as before, except we don't have to manage the servers, web server software, website deployment, or the load balancer.


#### Microservices

- [ ] Refactor Elastic Beanstalk(EB) website into ONLY providing an API. It should only have a POST/GET to update/retrieve that specific data from DynamoDB. 
- [ ] Bonus: Make it a simple REST API. Get rid of www.ourdomain.com and serve this EB as api.ourdomain.com
- [ ] Move most of the UI piece of our EB website into our Static S3 Website and use Javascript/whatever to retrieve the data from our api.ourdomain.com URL on page load. 
- [ ] Send data to the EB URL to have it update the DynamoDB. 
- [ ] Get rid of static.ourdomain.com and change our S3 Bucket to serve from www.ourdomain.com.

**Checkpoint:** EB deployment is now only a structured way to retrieve data from our database. All of UI and application logic is served from the S3 Bucket (via CloudFront). 
We can support many more users since we're no longer using expensive servers to serve the website's static data.


#### Serverless

- [ ] Write an AWS Lambda function to email a list of all of the Stock Symbols in the DynamoDB table every night. 
- [ ] Implement Least Privilege security for the Lambda Role. (Hint: Lambda using Python 3, Boto3, Amazon SES, scheduled with CloudWatch)
- [ ] Refactor the above app into a Serverless app. 

#### Serverless Arhitecture: 
1. Static S3 Website Front-End calls API Gateway which executes a Lambda Function which reads/updates data in the DyanmoDB table.
2. Use SSL enabled bucket as the primary domain landing page with static content.
3. Create an AWS API Gateway, use it to forward HTTP requests to an AWS Lambda function that queries the same data from DynamoDB as EB Microservice.
4. S3 static content should make Javascript calls to the API Gateway and then update the page with the retrieved data.
5. Once we have the "Get Stock Symbol" API Gateway + Lambda working, do the "New Symbol" API.

**Checkpoint:** API Gateway and S3 Bucket are fronted by CloudFront with SSL. We have no EC2 instances deployed. All work is done by AWS services and billed as consumed.

#### Cost Analysis

- [ ] Explore the AWS pricing models and see how pricing is structured for the services we've used.
- [ ] Answer the following for each of the main architectures we built:
    - Roughly how much would this have cost for a month?
    - How would we scale this architecture, and how would our costs change?

**Architectures**

*Basic Web Hosting:* HA EC2 Instances Serving Static Web Page behind ELB

*Microservices:* Elastic Beanstalk SSL Website for only API + S3 Static Website for all static content + DynamoDB Table + Route53 + CloudFront SSL

*Serverless:* Serverless Website using API Gateway + Lambda Functions + DynamoDB + Route53 + CloudFront SSL + S3 Static Website for all static content


#### Automation!

- [ ] Automate the deployment of the architectures above. 
- [ ] Use AWS CloudFormation or Terraform.
 
When we get each app-related section of the done by hand - go back and automate the provisioning of the infrastructure. 

For example: 
1. Automate the provisioning of EC2 instances. 
2. Automate the creation of S3 Bucket with Static Website Hosting enabled, etc. 

#### Continuous Delivery

- [ ] Develop a CI/CD pipeline to automatically update a dev deployment of the infrastructure when new code is published.
- [ ] Build a workflow to update the production version if approved. 
- [ ] Travis CI/Jenkins/CodePipeline are easy to go tools.

#### Other (optional)

- ~~Create complex IAM Policies. We would have had to do basic roles+policies for the EC2 Instance Role and Lambda Execution Role, but there are many advanced features.~~
- ~~Create a new VPC from scratch with multiple subnets, once that is working create another VPC and peer them together. Get a VM in each subnet to talk to each other using only their private IP addresses.~~
- [ ] Go back and redo the early EC2 instance goals but enable encryption on the disk volumes. Learn how to encrypt an AMI.

### Some open questions to answer
1. AWS Cloudform or Terraform?
2. EB or Kubernetes?
3. Replace DynamoDB with RDS (e.g. PostgreSQL, MySQL)?
