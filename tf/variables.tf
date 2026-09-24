variable "aws_region" {
  description = "AWS region for bucket."
  type        = string
  nullable    = false
}

variable "domain_name" {
  description = "Hostname."
  type        = string
  nullable    = false
}

variable "site_bucket_name" {
  description = "S3 bucket name for the static contents."
  type        = string
  nullable    = false
}

variable "acm_certificate_arn" {
  description = "ARN of an issued ACM certificate."
  type        = string
  nullable    = false
}
