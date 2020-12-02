
def get_users():	
	with open('/config/users.txt') as users_file:
	    return users_file.read().splitlines()
