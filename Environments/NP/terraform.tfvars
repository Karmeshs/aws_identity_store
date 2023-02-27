default_tags = {
  Environment          = "NP"
  CloudServiceProvider = "AWS"
  Availability         = "True"
  Backup               = "False"
}
### IAM role policy
role_name_ecs_execution = "task_role"
service_ecs_execution   = "ecs-tasks.amazonaws.com"

policy_name_ecs_execution        = "EcsTaskExecution-np"
policy_description_ecs_execution = "Policy for ECS task execution"

#Lambda role
service_lambda            = "lambda.amazonaws.com"
policy_description_lambda = "Policy for Lambda"

role_name_lambda_2   = "l1"
policy_name_lambda_2 = "L1"

