resource "aws_lambda_function" "handler" {
  function_name = "unsafe-handler"
  role          = "arn:aws:iam::123456789012:role/service-role/lambda-role"
  handler       = "index.handler"
  runtime       = "python3.12"
  filename      = "function.zip"

  environment {
    variables = {
      API_KEY = "plaintext-secret"
    }
  }
}
