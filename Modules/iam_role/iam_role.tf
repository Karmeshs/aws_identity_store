resource "aws_iam_role" "iar_role" {
  name               = var.role_name
  tags               = merge(var.default_tags, tomap({ "Name" = var.role_name }))
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "${var.service}"
      },
      "Action": "sts:AssumeRole"           
    }
  ]
}
EOF
}