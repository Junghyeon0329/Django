import openai
from rest_framework import response, status
from rest_framework.decorators import api_view

# OpenAI API 키 설정
openai.api_key = 'your-openai-api-key'

@api_view(['POST'])
def chatgpt_response(request):
    try:
        # 요청으로부터 사용자 메시지 가져오기
        user_message = request.data.get('message')

        if not user_message:
            return response.Response({"error": "No message provided"}, status=400)
        
        # ChatGPT에 요청 보내기 (최신 API 방식) - v0.28.0 
        res = openai.ChatCompletion.create(
            model="gpt-4",  # 또는 gpt-3.5 등 원하는 모델 사용
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        
        # ChatGPT의 응답을 추출하여 반환
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
                {"success": True, "message": f"{str(e)}."},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )