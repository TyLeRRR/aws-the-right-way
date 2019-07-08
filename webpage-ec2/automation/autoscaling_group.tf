provider "aws" {
  region = "eu-central-1"
}

resource "aws_autoscaling_group" "webpage-autoscaling" {
  name = "webpage-autoscaling"
  max_size = 2
  min_size = 2
  availability_zones = [
    "eu-central-1b",
    "eu-central-1a"]
  launch_configuration = "${aws_launch_configuration.webpage-launch-config.name}"
  health_check_type = "EC2"
  health_check_grace_period = 30
  load_balancers = [
    "${aws_elb.webpage-elb.name}"]
}

resource "aws_launch_configuration" "webpage-launch-config" {
  name = "webpage_launch_config"
  image_id = "ami-07f0f6e10c9a18895"
  instance_type = "t2.micro"
  iam_instance_profile = "ec2-r-w-s3"
  security_groups = ["sg-0a9bd08ed359e165f"]
  user_data = "${data.template_file.user-data.rendered}"
  root_block_device {
    delete_on_termination = true
  }
}

data "template_file" "user-data" {
  template = "${file("../install_prereq.sh")}"
}