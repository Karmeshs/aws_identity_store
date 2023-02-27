## Role-ECS execution
module "ecs_execution_role" {
  source       = "../../modules/iam_role"
  default_tags = var.default_tags
  role_name    = var.role_name_ecs_execution
  service      = var.service_ecs_execution
}
## Policy-ECS execution
module "ecs_execution_policy" {
  source             = "../../modules/iam_policy"
  default_tags       = var.default_tags
  policy_name        = var.policy_name_ecs_execution
  policy_description = var.policy_description_ecs_execution
  policy_template    = data.template_file.policy_ecstaskexecution_template.rendered
}
## PolicyAttachment-ECS execution
module "ecs_execution_policy_attach1" {
  source     = "../../modules/iam_policy_attach"
  policy_arn = module.ecs_execution_policy.policy_arn
  role_arn   = module.ecs_execution_role.role_id
}
### Role-lambda
module "lambda_role_2" {
  source       = "../../modules/iam_role"
  default_tags = var.default_tags
  role_name    = var.role_name_lambda_2
  service      = var.service_lambda
}
## Policy-lambda
module "lambda_policy_2" {
  source             = "../../modules/iam_policy"
  default_tags       = var.default_tags
  policy_name        = var.policy_name_lambda_2
  policy_description = var.policy_description_lambda
  policy_template    = data.template_file.policy_lambda_2.rendered
}
## PolicyAttachment-Lambda
module "lambda_policy_attach1" {
  source     = "../../modules/iam_policy_attach"
  policy_arn = module.lambda_policy_2.policy_arn
  role_arn   = module.lambda_role_2.role_id
}
module "lambda_policy_attach2" {
  source     = "../../modules/iam_policy_attach"
  policy_arn = data.aws_iam_policy.AWSLambdaVPCAccessExecutionRole.arn
  role_arn   = module.lambda_role_2.role_id
}
