
data "template_file" "sqs_policy" {
  template = file("scripts/sqs_policy.json")
  vars = {
    sqs_name = var.sqs1_name
  }
}
data "template_file" "dlq_policy" {
  template = file("scripts/sqs_policy.json")
  vars = {
    sqs_name = var.dlq2_name
  }
}
#SNS
data "template_file" "sns_policy" {
  template = file("scripts/sns_policy.json")
  vars = {
    sns_name = var.sns_name[0]
  }
}

data "aws_iam_policy" "AWSLambdaVPCAccessExecutionRole" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}