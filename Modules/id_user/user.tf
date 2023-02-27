resource "aws_identitystore_user" "user" {
  identity_store_id = var.identity_store_id

  display_name = var.display_name
  user_name    = var.user_name

  name {
    given_name  = var.first_name
    family_name = var.last_name
  }

  emails {
    value = var.email
  }
}