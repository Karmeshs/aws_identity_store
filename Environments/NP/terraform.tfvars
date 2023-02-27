tags = {
  Environment          = "NP"
  CloudServiceProvider = "AWS"
  Availability         = "True"
  Backup               = "False"
}

#identity sso
id_group_name  = "DEVS"
id_description = "Group for developers"

#ID user sso
user_name    = "Louis_king"
display_name = "Charles"
first_name   = "Louis"
last_name    = "King"
email        = "louis@gmail.com"

#Permission set 
permission_set_name= "Least_access"
permission_set_description= "Perm set to provide minimum access required"
session_duration= "PT2H"