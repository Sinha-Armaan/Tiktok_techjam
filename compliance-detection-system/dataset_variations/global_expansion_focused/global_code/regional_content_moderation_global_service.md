This architecture outlines a comprehensive, production-ready global implementation for Regional Content Moderation & Cultural Adaptation at a major social media company, designed for massive scale (100M+ users, 25+ countries, 50+ languages). It incorporates multi-region infrastructure, data sovereignty, localization, privacy automation, and robust testing, while intentionally including specific security/compliance vulnerabilities as requested.

---

## Global Architecture: Regional Content Moderation & Cultural Adaptation

**Feature ID:** `regional_content_moderation`
**Target Scale:** 100M+ global users, 25+ countries, 50+ languages (including RTL)
**Compliance:** GDPR, CCPA, PIPEDA, LGPD, and other regional data protection laws.
**Key Principles:** Data Residency, Least Privilege, Privacy by Design, Global-Local Balance, Automated Compliance.

---

### 1. Multi-Region Infrastructure Code (Terraform - AWS Example)

This section defines the infrastructure for deploying core services across multiple AWS regions, ensuring high availability, low latency, and regional compliance.

**Core Regions:** `us-east-1` (North America), `eu-west-1` (Europe), `ap-southeast-2` (APAC), `sa-east-1` (South America).

**Terraform Structure:**

```
.
├── main.tf                 # Global resources (Route 53, Global Accelerator)
├── variables.tf            # Global variables
├── outputs.tf              # Global outputs
├── modules/
│   ├── region_core/        # Reusable module for core regional infrastructure
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── moderation_service/ # Module for content moderation service deployment
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── ...                 # Other service-specific modules
├── environments/
│   ├── prod/
│   │   ├── us-east-1/
│   │   │   └── main.tf     # Deploys region_core and services in us-east-1
│   │   ├── eu-west-1/
│   │   │   └── main.tf     # Deploys region_core and services in eu-west-1
│   │   └── ...
│   └── dev/
│       └── ...
```

**`main.tf` (Global Resources - Example)**

```terraform
# Global Route 53 for DNS routing
resource "aws_route53_zone" "global_domain" {
  name = "socialmedia.com"
}

# Global Accelerator for intelligent traffic routing to regional endpoints
resource "aws_globalaccelerator_accelerator" "global_accelerator" {
  name            = "socialmedia-global-accelerator"
  ip_address_type = "IPV4"
  enabled         = true
}

resource "aws_globalaccelerator_listener" "http_listener" {
  accelerator_arn = aws_globalaccelerator_accelerator.global_accelerator.id
  port_range {
    from_port = 80
    to_port   = 80
  }
  protocol = "TCP"
}

resource "aws_globalaccelerator_listener" "https_listener" {
  accelerator_arn = aws_globalaccelerator_accelerator.global_accelerator.id
  port_range {
    from_port = 443
    to_port   = 443
  }
  protocol = "TCP"
}

# Regional Endpoints will be added to Endpoint Groups in regional Terraform configurations
```

**`modules/region_core/main.tf` (Regional Core Infrastructure - Example)**

```terraform
# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "${var.region}-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.region}-public-subnet-${count.index}"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + length(var.availability_zones))
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "${var.region}-private-subnet-${count.index}"
  }
}

# Regional Application Load Balancer (ALB)
resource "aws_lb" "app_lb" {
  name               = "${var.region}-app-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public[*].id
  enable_deletion_protection = true
  tags = {
    Name = "${var.region}-app-lb"
  }
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.acm_certificate_arn # Assumes ACM certificate is pre-provisioned
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default.arn
  }
}

resource "aws_lb_target_group" "default" {
  name     = "${var.region}-default-tg"
  port     = 8000 # Application port
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
  tags = {
    Name = "${var.region}-default-tg"
  }
}

# Regional Auto-Scaling Group for Content Moderation Service
resource "aws_launch_template" "moderation_lt" {
  name_prefix   = "${var.region}-moderation-lt"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.medium"
  key_name      = var.ssh_key_name
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    region = var.region
    # *** SECURITY ISSUE 1: Hardcoded API Key in User Data ***
    # This API key for a hypothetical external sentiment analysis service is directly embedded.
    # It should be fetched securely from AWS Secrets Manager or an equivalent.
    EXTERNAL_SENTIMENT_API_KEY = "sk_prod_1234567890abcdef"
  }))
  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 30
      volume_type = "gp2"
    }
  }
  tags = {
    Name = "${var.region}-moderation-instance"
  }
}

resource "aws_autoscaling_group" "moderation_asg" {
  name                      = "${var.region}-moderation-asg"
  vpc_zone_identifier       = aws_subnet.private[*].id
  desired_capacity          = 2
  max_size                  = 10
  min_size                  = 2
  launch_template {
    id      = aws_launch_template.moderation_lt.id
    version = "$Latest"
  }
  target_group_arns = [aws_lb_target_group.default.arn]
  health_check_type = "ELB"
  tags = [
    {
      key                 = "Name"
      value               = "${var.region}-moderation-asg"
      propagate_at_launch = true
    },
  ]
}

# Auto-scaling policies
resource "aws_autoscaling_policy" "cpu_scaling_up" {
  name                   = "${var.region}-cpu-scaling-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.moderation_asg.name
}

resource "aws_cloudwatch_metric_alarm" "