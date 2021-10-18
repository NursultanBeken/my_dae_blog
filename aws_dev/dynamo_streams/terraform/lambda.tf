data "archive_file" "lambda_zip" {
  count       = var.create_replica_proc ? 1 : 0
  type        = "zip"
  output_path = "lambda_function.zip"
  source {
    content  = file("../src/app.py")
    filename = "app.py"
  }
}

module "replication" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 2.0.0"
  create  = var.create_replica_proc

  function_name          = "db-replication-lambda"
  handler                = "app.handler"
  runtime                = "python3.8"
  publish                = true
  create_package         = false
  local_existing_package = var.create_replica_proc ? data.archive_file.lambda_zip[0].output_path : null

  cloudwatch_logs_kms_key_id    = module.cmk.key_arn
  create_role                   = true
  role_name                     = "db-replication-lambda-role"
  role_path                     = "/service-role/"
  attach_cloudwatch_logs_policy = false
  attach_policy_json            = true

  policy_json = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Sid = ""
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Effect   = "Allow"
          Resource = ["*"]
        },
        {
          Effect = "Allow"
          Action = [
            "dynamodb:BatchGet*",
            "dynamodb:DescribeStream",
            "dynamodb:DescribeTable",
            "dynamodb:Get*",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWrite*",
            "dynamodb:Update*",
            "dynamodb:PutItem",
            "dynamodb:ListStream",
            "dynamodb:DeleteItem"
          ]
          Resource = [
            "${module.dynamo_table.dynamodb_table_arn}/stream/*",
            module.dynamo_table.dynamodb_table_arn
          ]
        },
        {
          Effect = "Allow",
          Action = [
            "ssm:GetParameters",
            "ssm:GetParameter"
          ],
          Resource = [
            "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter${var.CREDS_PARAMETER_PATH}",
          ]
        }
      ]
    }
  )
  event_source_mapping = {
    dynamodb = {
      event_source_arn  = module.dynamo_table.dynamodb_table_stream_arn
      starting_position = "LATEST"
    }
  }
  environment_variables = {
    DYNAMO_DB_NAME       = module.dynamo_table.dynamodb_table_id,
    CREDS_PARAMETER_PATH = var.CREDS_PARAMETER_PATH
  }

}