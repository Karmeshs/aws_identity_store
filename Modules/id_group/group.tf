resource "aws_identitystore_group" "group" {
  display_name      = var.name
  description       = var.description
  identity_store_id = var.identity_store_id #"d-9f67175385"
}