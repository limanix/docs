locals {
  domain_labels        = split(".", var.domain_name)
  name_prefix          = join("-", reverse(slice(local.domain_labels, 0, length(local.domain_labels) - 1)))
  cloudfront_origin_id = "s3-${var.site_bucket_name}"

  content_security_policy = join("; ", [
    "default-src 'self'",
    "base-uri 'self'",
    "connect-src 'self'",
    "font-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "img-src 'self' data:",
    "media-src 'self'",
    "object-src 'none'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
  ])

  tags = {
    ManagedBy  = "Terraform"
    Project    = "limanix"
    Repository = "limanix/docs"
    Site       = var.domain_name
  }
}
