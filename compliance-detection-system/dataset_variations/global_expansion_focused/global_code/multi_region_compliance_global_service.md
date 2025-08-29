This document outlines a comprehensive, production-ready global architecture for a social media company's Multi-Region Data Compliance System. It addresses the requirements for global expansion, supporting 25+ countries, 50+ languages, and handling 100M+ users while adhering to strict data sovereignty and privacy regulations like GDPR, CCPA, PIPEDA, and LGPD.

**IMPORTANT NOTE:** As requested, this implementation intentionally includes **four (4) code-level security/compliance issues** that should be flagged in a real-world audit:

1.  **Hardcoded Secret:** A database password is hardcoded in `services/data_sovereignty_service.py`.
2.  **SQL Injection Vulnerability:** The `get_user_data` endpoint in `services/privacy_compliance_service.py` uses unsanitized input directly in a SQL query.
3.  **Insecure HTTP Connection:** The `data_sovereignty_service.py` communicates with an internal compliance service over plain HTTP.
4.  **Poor Error Handling:** The `global_api_gateway.py` (conceptual, but demonstrated in a Flask app) returns raw stack traces on unhandled exceptions.

---

## Global Architecture Overview

The system is designed as a distributed microservices architecture, deployed across multiple AWS regions (e.g., `us-east-1`, `eu-west-1`, `ap-southeast-2`). Each region operates largely independently for core user data processing, with global services handling routing, authentication, and cross-region coordination.

**Key Principles:**
*   **Data Residency by Design:** User data is primarily stored and processed within the user's declared or inferred region of residence.
*   **Global-Local Hybrid:** Global services for routing, authentication, and configuration, with regional services for data processing and storage.
*   **Automated Compliance:** Built-in checks and automation for privacy regulations.
*   **Scalability & Resilience:** Auto-scaling, multi-AZ deployments, cross-region replication, and failover.
*   **Localization & Cultural Adaptation:** Support for diverse languages and cultural nuances.

---

## 1. Multi-Region Infrastructure Code (Terraform)

This section outlines the Terraform structure for deploying regional infrastructure and global components.

```terraform
# main.tf - Global Orchestration
# This file orchestrates the deployment of global resources and regional modules.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "socialmedia-terraform-state-global"
    key            = "global/terraform.tfstate"
    region         = "us-east-1" # Central region for global state
    encrypt        = true
    dynamodb_table = "socialmedia-terraform-state-lock-global"
  }
}

provider "aws" {
  region = "us-east-1" # Default provider for global resources
}

# Global Resources
# -----------------------------------------------------------------------------

# Global DNS (Route 53)
resource "aws_route53_zone" "primary" {
  name = "socialmedia.com"
}

# Global Load Balancer (AWS Global Accelerator)
# Directs traffic to optimal regional endpoints based on user location and health.
resource "aws_globalaccelerator_accelerator" "global_app_accelerator" {
  name            = "socialmedia-global-accelerator"
  ip_address_type = "IPV4"
  enabled         = true
  attributes {
    flow_logs_enabled   = true
    flow_logs_s3_bucket = "socialmedia-global-logs"
    flow_logs_s3_prefix = "global-accelerator-logs/"
  }
}

resource "aws_globalaccelerator_listener" "http_listener" {
  accelerator_arn = aws_globalaccelerator_accelerator.global_app_accelerator.id
  port_range {
    from_port = 80
    to_port   = 80
  }
  protocol = "TCP"
}

resource "aws_globalaccelerator_listener" "https_listener" {
  accelerator_arn = aws_globalaccelerator_accelerator.global_app_accelerator.id
  port_range {
    from_port = 443
    to_port   = 443
  }
  protocol = "TCP"
}

# Cross-Region Networking (Transit Gateway for complex scenarios, VPC Peering for simpler)
# For a global company, Transit Gateway is preferred for scalability and management.
resource "aws_ec2_transit_gateway" "global_tgw" {
  description                     = "Global Transit Gateway for cross-region connectivity"
  amazon_side_asn                 = 64512 # Example ASN
  auto_accept_shared_attachments  = "disable"
  default_route_table_association = "enable"
  default_route_table_propagation = "enable"
  tags = {
    Name = "socialmedia-global-tgw"
  }
}

# Regional Deployments (Modules)
# -----------------------------------------------------------------------------

# Define regions to deploy to
locals {
  regions = {
    "us-east-1"    = { country_codes = ["US", "CA"], default_language = "en" }
    "eu-west-1"    = { country_codes = ["GB", "FR", "DE", "IE"], default_language = "en" }
    "ap-southeast-2" = { country_codes = ["AU", "NZ"], default_language = "en" }
    # Add more regions as needed for 25+ countries
  }
}

# Deploy regional infrastructure using a module for each region
module "regional_deployments" {
  source = "./modules/region_stack" # Path to the regional module
  for_each = local.regions

  region_name        = each.key
  country_codes      = each.value.country_codes
  default_language   = each.value.default_language
  global_tgw_id      = aws_ec2_transit_gateway.global_tgw.id
  global_accelerator_http_listener_arn = aws_globalaccelerator_listener.http_listener.id
  global_accelerator_https_listener_arn = aws_globalaccelerator_listener.https_listener.id
}

output "global_accelerator_dns_name" {
  description = "DNS name of the Global Accelerator"
  value       = aws_globalaccelerator_accelerator.global_app_accelerator.dns_name
}

output "regional_app_endpoints" {
  description = "Application endpoints for each region"
  value       = { for k, v in module.regional_deployments : k => v.app_load_balancer_dns }
}
```

```terraform
# modules/region_stack/main.tf - Regional Infrastructure Module
# This module defines the infrastructure for a single AWS region.

variable "region_name" {
  description = "The AWS region to deploy resources into."
  type        = string
}

variable "country_codes" {
  description = "List of country codes primarily served by this region."
  type        = list(string)
}

variable "default_language" {
  description = "Default language for this region."
  type        = string
}

variable "global_tgw_id" {
  description = "ID of the Global Transit Gateway for cross-region peering."
  type        = string
}

variable "global_accelerator_http_listener_arn" {
  description = "ARN of the Global Accelerator HTTP listener."
  type        = string
}

variable "global_accelerator_https_listener_arn" {
  description = "ARN of the Global Accelerator HTTPS listener."
  type        = string
}

provider "aws" {
  region = var.region_name
  alias  = var.region_name # Use alias for regional providers
}

# Regional Backend for Terraform State
terraform {
  backend "s3" {} # Configuration will be passed via CLI or environment variables
}

# Regional VPC
resource "aws_vpc" "app_vpc" {
  provider   = aws.${var.region_name}
  cidr_block = "10.0.0.0/16" # Example CIDR, adjust per region
  tags = {
    Name        = "socialmedia-${var.region_name}-vpc"
    Environment = "prod"
  }
}

# Subnets (Public, Private, Database)
resource "aws_subnet" "public" {
  provider          = aws.${var.region_name}
  count             = 2 # Multi-AZ
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "10.0.${count.index}.0/24" # Example
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "socialmedia-${var.region_name}-public-subnet-${count.index}"
  }
}

resource "aws_subnet" "private" {
  provider          = aws.${var.region_name}
  count             = 2
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24" # Example
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "socialmedia-${var.region_name}-private-subnet-${count.index}"
  }
}

resource "aws_subnet" "database" {
  provider          = aws.${var.region_name}
  count             = 2
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "10.0.${count.index + 20}.0/24" # Example
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "socialmedia-${var.region_name}-database-subnet-${count.index}"
  }
}

data "aws_availability_zones" "available" {
  provider = aws.${var.region_name}
  state    = "available"
}

# Regional Load Balancer (Application Load Balancer)
resource "aws_lb" "app_lb" {
  provider           = aws.${var.region_name}
  name               = "socialmedia-${var.region_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public[*].id
  tags = {
    Name = "socialmedia-${var.region_name}-alb"
  }
}

resource "aws_lb_listener" "http_listener" {
  provider          = aws.${var.region_