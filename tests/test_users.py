import requests
import os

endpoint = "http://localhost:5000"

def test_user_login_wrong_password():
	payload = {
		"username": "paulclrt", #good username
		"password": "wrongpassword"
	}
	req = requests.post(f"{endpoint}/api/users/login", json=payload)
	assert req.status_code == 401 and req.json() == {"msg": "Bad username or password"}

def test_user_login_user_does_not_exists():
	payload = {
		"username": "userdoesnotexists", #non existtant
		"password": "pass2"
	}
	req = requests.post(f"{endpoint}/api/users/login", json=payload)
	assert req.status_code == 401 and req.json() == {"msg": "Bad username or password"}

def test_user_login_good_password():
	payload = {
		"username": "paulclrt", #good username
		"password": "pass2" # good password
	}
	req = requests.post(f"{endpoint}/api/users/login", json=payload)
	assert req.status_code == 200 and req.json() == {"msg": "Logged in"} and req.headers['Set-Cookie'] is not None


def test_user_logout():
	req = requests.post(f"{endpoint}/api/users/logout", headers={"Cookie": "session=junk"})
	assert req.headers["Set-Cookie"] == 'session=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/'



def test_register_normal():
	payload = {
		"username": "test_account_" + str(os.urandom(20)), # should not exists already in db
		"email": "test_account_" + str(os.urandom(20)) + "@gmail.com",
		"password": "doesn't matter"
	}
	req = requests.post(f"{endpoint}/api/users/register", json=payload)
	assert req.status_code == 201 and req.json() == {"msg": "User registered"}


def test_register_username_already_used():
	payload = {
		"username": "paulclrt", # should already exists in db
		"email": "test_account_" + str(os.urandom(20)) + "@gmail.com",
		"password": "doesn't matter"
	}
	req = requests.post(f"{endpoint}/api/users/register", json=payload)
	assert req.status_code == 400 and req.json() == {"msg": "User already exists"}

def test_register_email_already_used():
	payload = {
		"username": "test_account_" + str(os.urandom(20)), 
		"email": "p4ul.claret@mail.com", # should already exists in db
		"password": "doesn't matter"
	}
	req = requests.post(f"{endpoint}/api/users/register", json=payload)
	assert req.status_code == 400 and req.json() == {"msg": "User already exists"}




def create_temp_account():
	payload = {
		"username": "test_account_" + str(os.urandom(20)), 
		"email": "test_account_" + str(os.urandom(20)) + "@mail.com",
		"password": "password"
	}
	req = requests.post(f"{endpoint}/api/users/register", json=payload)
	if req.status_code == 201:
		return payload
	else:
		raise Exception("Could not create account for test case")

def login_into_account(account_details):
	payload = {
		"username": account_details['username'],
		"password": account_details['password']
	}
	req = requests.post(f"{endpoint}/api/users/login", json=payload)
	if req.status_code == 200:
		login_cookie = req.headers["Set-Cookie"].split("; ")[0]
		return login_cookie
	else:
		raise Exception("Could not login into temp account for test case")


def test_delete_account_normal():
	"""First create a temp account that we will delete"""

	a_details = create_temp_account()
	session_cookie = login_into_account(a_details)

	param = {"username": a_details["username"]}
	req = requests.delete(f"{endpoint}/api/users/delete", params=param, cookies={"session": session_cookie.split("=")[1]})
	try:
		assert req.status_code == 200 and req.json() == {"msg": "User deleted successfully"}
	except:
		# in case deletion failed, delte manualy wih info bellow
		print("delte manually please:")
		print("FAILED ACCOUNT DELETION:", a_details)

def test_delete_account_other_user_that_exists():
	"""First create a temp account that we will delete"""
	a_details = create_temp_account()
	session_cookie = login_into_account(a_details)

	param = {"username": "paulclrt"}
	req = requests.delete(f"{endpoint}/api/users/delete", params=param, cookies={"session": session_cookie.split("=")[1]})
	try:
		assert req.status_code == 403 and req.json() == {"msg": "Unauthorized or user does not exist"}
	except:
		# in case deletion failed, delte manualy wih info bellow
		print("delte manually please:")
		print("FAILED ACCOUNT DELETION:", a_details)




def test_delete_account_other_user_that_doesnt_exists():
	"""First create a temp account that we will delete"""
	a_details = create_temp_account()
	session_cookie = login_into_account(a_details)

	param = {"username": str(os.urandom(10))}
	req = requests.delete(f"{endpoint}/api/users/delete", params=param, cookies={"session": session_cookie.split("=")[1]})
	try:
		assert req.status_code == 403 and req.json() == {"msg": "Unauthorized or user does not exist"}
	except:
		# in case deletion failed, delte manualy wih info bellow
		print("delte manually please:")
		print("FAILED ACCOUNT DELETION:", a_details)

def test_delete_account_with_being_authed():
	"""First create a temp account that we will delete"""

	param = {"username": "paulclrt"} #username exists
	req = requests.delete(f"{endpoint}/api/users/delete", params=param)
	assert req.status_code == 400 and req.json() == {"msg": "Missing username or user_id"}


def test_delete_account_without_being_authed():
	"""First create a temp account that we will delete"""
	a_details = create_temp_account()

	param = {"username": a_details["username"]} #username exists
	req = requests.delete(f"{endpoint}/api/users/delete", params=param)
	try:
		assert req.status_code == 400 and req.json() == {"msg": "Missing username or user_id"}
	except:
		# in case deletion failed, delte manualy wih info bellow
		print("delte manually please:")
		print("FAILED ACCOUNT DELETION:", a_details)