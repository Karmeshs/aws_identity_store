
# data "template_file" "policy" {
#   template = file("scripts/policy.json")
#   vars = {
#     name = var.name
#   }
# }

data "aws_ssoadmin_instances" "sso" {}