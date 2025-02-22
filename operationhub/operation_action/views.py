from rest_framework import response, status, decorators
import workforce_API
    
@decorators.api_view(['POST'])
def homepage_login(request):
    
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return response.Response({
            "success": False, "message": "Lack of login information."},
            status=status.HTTP_400_BAD_REQUEST
        )
    Authentication = workforce_API.JWTAuthentication()
    return Authentication.login(request)

import openai
openai.api_key = 'your-openai-api-key' # OpenAI API 키 설정
@decorators.api_view(['POST'])
def chatgpt_response(request):
    try:
        # 요청으로부터 사용자 메시지 가져오기
        user_message = request.data.get('message')

        if not user_message:
            return response.Response({"error": "No message provided"}, status=400)
        
        res = openai.ChatCompletion.create(
            model="gpt-4",  # 또는 gpt-3.5 등 원하는 모델 사용
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        chatgpt_reply = res['choices'][0]['message']['content']     
        
        return response.Response(
            {
                "success": True,
                "message": f"{chatgpt_reply}"
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return response.Response(
            {"success": False, "message": f"Error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )