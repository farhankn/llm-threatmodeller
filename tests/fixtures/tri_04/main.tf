resource "aws_iam_policy" "wildcard_admin" {
  name = "wildcard-admin"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
