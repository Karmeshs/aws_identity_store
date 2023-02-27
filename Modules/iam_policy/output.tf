output "policy_arn" {
  value       = aws_iam_policy.policy.arn
  description = "The arn of the policy."
}