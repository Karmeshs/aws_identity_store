resource "aws_identitystore_group_membership" "membership" {
  identity_store_id = var.identity_store_id
  group_id          = var.group_id
  member_id         = var.user_id
}