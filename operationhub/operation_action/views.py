import openai
from rest_framework import response, status
from rest_framework.decorators import api_view
from transformers import pipeline, AutoTokenizer

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# GPT-2 모델과 tokenizer 로드
generator = pipeline("text-generation", model="gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 새로운 패딩 토큰 추가
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# 패딩 토큰을 설정
tokenizer.pad_token = '[PAD]'


openai.api_key = 'your-openai-api-key' # OpenAI API 키 설정

@api_view(['POST'])
def chatgpt_response(request):
    try:
        # 요청으로부터 사용자 메시지 가져오기
        user_message = request.data.get('message')

        if not user_message:
            return response.Response({"error": "No message provided"}, status=400)
        
        # res = openai.ChatCompletion.create(
        #     model="gpt-4",  # 또는 gpt-3.5 등 원하는 모델 사용
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": user_message},
        #     ],
        # )
        # chatgpt_reply = res['choices'][0]['message']['content']     
        
        # 로컬 GPT-2 모델을 사용하여 응답 생성
        gpt2_response = generator(
            user_message, 
            max_length=50, 
            truncation=True,  # 길이 초과시 자르기
            temperature=0.7,
            num_return_sequences=1
            )
                
        chatgpt_reply = gpt2_response[0]['generated_text']        
                       
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
        
