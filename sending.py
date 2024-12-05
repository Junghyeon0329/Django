import requests
import sys

def send_api_request_post(url, headers, body):
    try:
        # POST 요청을 보내는 예시 (기타 GET, PUT, DELETE 요청으로도 수정 가능)
        response = requests.post(url, headers=headers, json=body)

        # 요청이 성공했는지 확인
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
    try:
        # GET 요청을 보낼 때는 'params' 인자를 사용하여 쿼리 파라미터를 전달
        response = requests.get(url, headers=headers, params=params)

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            print("Request was successful")
            return response.json()  # 응답을 JSON 형식으로 반환
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

url = "http://127.0.0.1:8000/api/token/"

body = {"username": "admin","password": "test"}
response = send_api_request_post(url, None, body)
if response:
    access_token = response['access']
else: 
    print("recieve access token")
    sys.exit()    

url = "http://127.0.0.1:8000/users/"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
params = {"email_id": ""}

# GET 요청을 보낼 때는 params로 쿼리 파라미터를 전달
response = send_api_request_get(url, headers, params)
print(response)

