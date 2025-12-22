# resource "aws_iam_role" "agentcore_lambda_role" {
#   name = "agentcore-dev-agent-lambda-role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Principal = {
#           Service = "lambda.amazonaws.com"
#         }
#         Action = "sts:AssumeRole"
#       }
#     ]
#   })
# }

# resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
#   role       = aws_iam_role.agentcore_lambda_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
# }

# Archive the lambda source into a zip file
data "archive_file" "agentcore_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../services/agent/src"
  output_path = "${path.module}/agentcore-dev-agent.zip"
}

resource "aws_lambda_function" "agentcore_dev_agent" {
  function_name = "agentcore-dev-agent"

  role          = "arn:aws:iam::316761693639:role/agentcore-dev-agent-lambda-role"

  handler       = "handler.lambda_handler"
  runtime       = "python3.11"

  filename         = data.archive_file.agentcore_lambda_zip.output_path
  source_code_hash = data.archive_file.agentcore_lambda_zip.output_base64sha256

  timeout = 10
}
