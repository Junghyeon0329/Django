import requests
import sys

# Global variable to store access_token
access_token = None

# ========================
# Helper functions
# ========================

def send_api_request_post(url, headers, body):
	"""POST 요청을 보내는 함수"""
	try:
		response = requests.post(url, headers=headers, json=body)
		if response.status_code == 200:
			print("Request was successful")
			return response.json()  # 응답을 JSON 형식으로 반환
		else:
			print(f"Error {response.status_code}: {response.text}")
			return None
	except requests.exceptions.RequestException as e:
		print(f"An error occurred: {e}")
		return None
	
def send_api_request_get(url, headers, params):
	"""GET 요청을 보내는 함수"""
	try:
		response = requests.get(url, headers=headers, params=params)
		if response.status_code == 200:
			print("Request was successful")
			return response.json()  # 응답을 JSON 형식으로 반환
		else:
			print(f"Error {response.status_code}: {response.text}")
			return None
	except requests.exceptions.RequestException as e:
		print(f"An error occurred: {e}")
		return None
	
def send_api_request_delete(url, headers, params = None):
	"""DELETE 요청을 보내는 함수"""
	try:
		response = requests.delete(url, headers=headers, params=params)
		if response.status_code == 200:
			print("Request was successful")
			return response.json()  # 응답을 JSON 형식으로 반환
		else:
			print(f"Error {response.status_code}: {response.text}")
			return None
	except requests.exceptions.RequestException as e:
		print(f"An error occurred: {e}")
		return None    

# ========================
# Authentication functions
# ========================

def get_access_token():
	"""Access token을 받아오는 함수"""
	global access_token  # Global access_token을 사용
	if access_token:
		print("You already have an access token.")
		return access_token  # 이미 토큰이 있으면 반환

	url = "http://127.0.0.1:8000/api/token/"
	body = {
		"username": input("Enter username: "),
		"password": input("Enter password: ")
	}
	response = send_api_request_post(url, None, body)
	if response:
		access_token = response['access']
		return access_token
	else:
		print("Failed to receive access token")

def login_user():
	"""유저 로그인 함수"""
	global access_token
	url = "http://127.0.0.1:8000/login/"
	body = {
		"username": input("Enter username: "),
		"password": input("Enter password: "),
	}
	response = send_api_request_post(url, headers=None, body=body)
	if response:
		access_token = response['access']
		return access_token
	else:
		print("Failed to receive access token")

# ========================
# User-related API functions
# ========================

def get_user_by_email():
	"""Email로 유저 정보를 조회하는 함수"""
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/users/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}
	params = {"email_id": input("Enter email ID to search: ")}
	response = send_api_request_get(url, headers, params)
	print("User info: ", response)

def create_user():
	"""새 유저를 생성하는 함수"""
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/info/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}
	body = {
		"username": input("Enter username: "),
		"email": input("Enter email: "),
		"password": input("Enter password: "),
		"is_superuser" : False,
		"is_staff" : False
	}
	response = send_api_request_post(url, headers, body)
	print("Created user: ", response)
	
def reset_password():
	"""비밀번호를 초기화하는 함수"""
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/info/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}
	params = {
		"email_id": input("Enter email: "),
		"new_password": input("Enter new password: "),
	}
	response = send_api_request_get(url, headers, params)
	print("Password reset: ", response)

def Withdrawal():
	"""유저 회원탈퇴 함수"""
	global access_token
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/info/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}
	response = send_api_request_delete(url, headers)
	if response:
		print("User deleted successfully.")
		# 탈퇴 후 유저 메뉴로 돌아가기
		access_token = None
		main()
	else:
		print("Failed to delete user.")

def create_board():
	"""게시판 작성"""
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/board/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}
	body = {
		"title": input("Enter title: "),
		"content": input("Enter content: ")
	}
	response = send_api_request_post(url, headers, body)
	print("Post board: ", response)
	
def search_board():
	"""게시판 검색"""
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/board/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}

	# user_id를 입력받을 때, 입력이 없으면 None으로 처리
	user_id = input("User ID (optional, press Enter to skip): ").strip()

	# user_id가 입력되었을 경우에만 params에 추가
	params = {}
	if user_id:
		params["user_id"] = user_id

	# API 요청 보내기
	response = send_api_request_get(url, headers, params)
	print("Board content: ", response)

def delete_board():
	"""게시판 삭제"""
	if not access_token:
		print("Access token is required. Please get the token first.")
		return  # 토큰이 없으면 실행하지 않음

	url = "http://127.0.0.1:8000/board/"
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	}

	# user_id를 입력받을 때, 입력이 없으면 None으로 처리
	params = {
		"board_id": input("Enter board_id: "),
	}
	# API 요청 보내기
	response = send_api_request_delete(url, headers, params)
	if response:
		print("board deleted successfully.")
	else:
		print("Failed to delete board.")

# ========================
# Main function (Menu)
# ========================

def user_menu():
	"""유저 관련 메뉴"""
	while True:
		print("\nUser Information Menu:")
		print("1. Create User")
		print("2. Reset Password")
		print("3. Withdrawal")
		print("4. Search User by Email")
		print("5. Back to Main Menu")

		choice = input("Enter your choice (1/2/3/4/5): ")

		if choice == '1':
			create_user()
		elif choice == '2':
			reset_password()
		elif choice == '3':
			Withdrawal()
		elif choice == '4':
			get_user_by_email()
		elif choice == '5':
			break  # Main menu로 돌아가기
		else:
			print("Invalid choice. Please try again.")

def board_menu():
	"""게시판 관련 메뉴"""
	while True:
		print("\nBoard Menu:")
		print("1. Create Board")
		print("2. Search Board")
		print("3. Delete Board")
		print("3. Back to Main Menu")

		choice = input("Enter your choice (1/2/3/4): ")

		if choice == '1':
			create_board()
		elif choice == '2':
			search_board()
		elif choice == '3':
			delete_board()
		elif choice == '4':
			break  # Main menu로 돌아가기
		else:
			print("Invalid choice. Please try again.")

def main():
	"""메인 함수 - 사용자가 선택한 옵션에 따라 다른 작업을 수행"""
	global access_token
	while True:
		if not access_token:  # Access token이 없으면 1번을 먼저 하라는 메시지를 출력
			print("\nPlease get an Access Token first by selecting option 1.")
		
		print("\nChoose an option:")
		print("1. Login")
		print("2. User Information")
		print("3. Board")
		print("4. Exit")

		choice = input("Enter your choice (1/2/3/4): ")

		if choice == '1':
			access_token = login_user()  # 로그인 시 토큰 받기
		elif choice == '2':
			if access_token:  # 토큰이 없으면 메뉴 진행 안됨
				user_menu()  # 유저 관련 메뉴로 이동
			else:
				print("Please get an Access Token first (Option 1).")
		elif choice == '3':
			if access_token:  # 토큰이 없으면 메뉴 진행 안됨
				board_menu()  # 게시판 메뉴로 이동
			else:
				print("Please get an Access Token first (Option 1).")
		elif choice == '4':
			print("Exiting.")
			sys.exit()
		else:
			print("Invalid choice. Please try again.")

if __name__ == "__main__":
	main()