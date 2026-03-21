resource "aws_s3_bucket" "public_bucket" {
  bucket = "public-demo-bucket"
  acl    = "public-read"
}
