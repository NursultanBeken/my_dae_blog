module "dynamo_table" {

  source  = "terraform-aws-modules/dynamodb-table/aws"
  version = "~> 1.0"

  name = "test-replica-db-table"

  hash_key  = "account_id"
  range_key = "partition"

  server_side_encryption_enabled     = true
  server_side_encryption_kms_key_arn = module.cmk.key_arn

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attributes = [
    {
      name = "account_id"
      type = "S"
    },
    {
      name = "partition"
      type = "S"
    }
  ]
}