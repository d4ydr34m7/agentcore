# S3 
resource "aws_s3_bucket" "data" {
  bucket        = "${local.name_prefix}-data"
  force_destroy = false  
}

# Basic server-side encryption + block public access
resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudWatch log group 
resource "aws_cloudwatch_log_group" "app" {
  name              = "/${local.name_prefix}/app"
  retention_in_days = 14
}
