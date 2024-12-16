import requests
import sys

BASE_URL = "http://127.0.0.1:8000"  # API의 기본 URL
access_token = None

# ========================
# Helper functions
# ========================
def send_api_request(method, url, headers, body=None, params=None):
    """API 요청을 보내는 함수"""
    try:
        response = requests.request(method, url, headers=headers, json=body, params=params)
        if response.status_code == 200:
            print(f"{method} Request was successful")
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

"""유저 로그인 함수"""
def login_user():
    
    global access_token
    url = f"{BASE_URL}/login/"
    body = {
        "email": input("Enter email: "),
        "password": input("Enter password: "),
    }
    print()
    response = send_api_request("POST", url, headers=None, body=body)
    if response:
        access_token = response['access']
        return access_token
    else:
        print("Failed to receive access token")
        return None

# ========================
# User-related API functions(usermanage.py)
# ========================

"""새 유저를 생성하는 함수"""
def create_user():
   
    url = f"{BASE_URL}/user/"
    body = {
        "email": input("Enter email: "),
        "password": input("Enter password: "),
        "is_superuser": False,
        "is_staff": False
    }
    print()
    response = send_api_request("POST", url, headers=None, body=body)
    print("Created user: ", response)
    
"""비밀번호를 초기화하는 함수"""
def reset_password():
   
    if not access_token:
        print("Access token is required. Please get the token first.")
        return

    url = f"{BASE_URL}/user/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "email": input("Enter email: "),
        "current_password": input("Enter current password: "),
        "new_password": input("Enter new password: ")
    }
    print()
    response = send_api_request("PUT", url, headers=headers, body=body)
    print("Password reset: ", response)
    
"""유저 회원탈퇴 함수"""
def withdrawal():
    
    global access_token
    if not access_token:
        print("Access token is required. Please get the token first.")
        return

    url = f"{BASE_URL}/user/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = send_api_request("DELETE", url, headers=headers)
    if response:
        print("User deleted successfully.")
        # 탈퇴 후 유저 메뉴로 돌아가기
        access_token = None
        main()
    else:
        print("Failed to delete user.")

# ========================
# Board-related API functions
# ========================

"""게시판 작성"""
def create_board():
 
    if not access_token:
        print("Access token is required. Please get the token first.")
        return

    url = f"{BASE_URL}/board/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "title": input("Enter title: "),
        "content": input("Enter content: ")
    }
    print()
    response = send_api_request("POST", url, headers=headers, body=body)
    print("Post board: ", response)

"""게시판 검색"""
def search_board():

    if not access_token:
        print("Access token is required. Please get the token first.")
        return

    url = f"{BASE_URL}/board/"
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
    response = send_api_request("GET", url, headers=headers, params=params)
    print("Board content: ", response)

"""게시판 삭제"""
def delete_board():

    if not access_token:
        print("Access token is required. Please get the token first.")
        return

    url = f"{BASE_URL}/board/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "board_id": input("Enter board_id: "),
    }
    print()
    response = send_api_request("DELETE", url, headers=headers, params=params)
    if response:
        print("Board deleted successfully.")
    else:
        print("Failed to delete board.")

# ========================
# Main function (Menu)
# ========================

def board_menu():
    """게시판 관련 메뉴"""
    while True:
        print("\nBoard Menu:")
        print("1. Create Board")
        print("2. Search Board")
        print("3. Delete Board")
        print("4. Back to Main Menu")

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
        print("1. 로그인")
        print("2. 회원가입")
        print("3. 회원탈퇴")
        print("4. 비밀번호변경")        
        print("5. 게시판")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            access_token = login_user()  # 로그인 시 토큰 받기
            
        elif choice == '2': create_user()
        
        elif choice == '3':
            if access_token: withdrawal()  
            else:
                print("Please get an Access Token first (Option 1).")
                
        elif choice == '4':
            if access_token: reset_password()  
            else:
                print("Please get an Access Token first (Option 1).")
                
        elif choice == '5':
            if access_token: board_menu()  
            else:
                print("Please get an Access Token first (Option 1).")
                
        elif choice == '6':
            print("Exiting.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
