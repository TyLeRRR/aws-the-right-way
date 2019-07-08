resource "aws_elb" "webpage-elb" {
  name = "webpage-elb"
  availability_zones = ["eu-central-1b", "eu-central-1a"]
  security_groups = []
  listener {
    instance_port = 80
    instance_protocol = "http"
    lb_port = 80
    lb_protocol = "http"
  }

  health_check {
    healthy_threshold   = 10
    unhealthy_threshold = 4
    timeout             = 15
    target              = "HTTP:80/index.html"
    interval            = 30
  }
}

output "elb_ip" {
  value = aws_elb.webpage-elb.dns_name
  description="Endpoint to connect to our webpage."
}