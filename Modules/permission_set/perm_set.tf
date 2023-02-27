resource "aws_ssoadmin_permission_set" "example" {
  name         = var.name
  description  = var.description
  instance_arn = var.instance_arn
  # relay_state      = "https://s3.console.aws.amazon.com/s3/home?region=us-east-1#"
  session_duration = var.session_duration
  tags             = var.tags
}
