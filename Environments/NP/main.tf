
module "id_group" {
  source            = "../../modules/id_group"
  identity_store_id = tolist(data.aws_ssoadmin_instances.sso.identity_store_ids)[0]
  description       = var.id_description
  name              = var.id_group_name
}
module "id_user" {
  source            = "../../modules/id_user"
  identity_store_id = tolist(data.aws_ssoadmin_instances.sso.identity_store_ids)[0]
  user_name         = var.user_name
  display_name      = var.display_name
  first_name        = var.first_name
  last_name         = var.last_name
  email             = var.email
}
module "id_group_membership" {
  source            = "../../modules/id_group_membership"
  identity_store_id = tolist(data.aws_ssoadmin_instances.sso.identity_store_ids)[0]
  group_id          = module.id_group.id
  user_id           = module.id_user.id
}
module "permission_set" {
  source            = "../../modules/permission_set"
  instance_arn     = tolist(data.aws_ssoadmin_instances.sso.arns)[0]
  description       = var.id_description
  name              = var.id_group_name
  tags =var.tags
}
