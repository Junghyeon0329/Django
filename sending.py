import requests
import sys

# Global variable to store access_token
access_token = None

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
        # print(f"Access Token: {access_token}")
        return access_token
    else:
        print("Failed to receive access token")
        # sys.exit()

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
    print("Created user: ", response)

def login_user():
    """유저 로그인 함수"""
    url = "http://127.0.0.1:8000/login/"
    
    body = {
        "username": input("Enter username: "),
        # "email": input("Enter email: "),
        "password": input("Enter password: "),
    }
    response = send_api_request_post(url, headers = None, body=body)
    if response:
        access_token = response['access']
        # print(f"Access Token: {access_token}")
        return access_token
    else:
        print("Failed to receive access token")
        # sys.exit()
        
def main():
    """메인 함수 - 사용자가 선택한 옵션에 따라 다른 작업을 수행"""
    global access_token
    while True:
        # 메뉴 출력
        print()
        print("Choose an option:")
        print("1. Get Access Token")
        print("2. Create user")
        print("3. Reset password")
        print("4. Login user")
        print("5. Search user by email")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            access_token = get_access_token()
            
        elif choice == '2':
            if not access_token:
                print("Access token is required. Please get the token first.")
            else: create_user()
        
        elif choice == '3':
            if not access_token:
                print("Access token is required. Please get the token first.")
            else: reset_password()  
                
        elif choice == '4':
            access_token = login_user()  
              
        elif choice == '5':
            if not access_token:
                print("Access token is required. Please get the token first.")
            else: get_user_by_email()
        else:
            print("Invalid choice. Exiting.")
            # sys.exit()

if __name__ == "__main__":
    main()
