'''
    urlpatterns = [
        path("permissions/", PermissionViewSet.as_view({
            "get": "list", #모든 객체의 리스트 반환
            "post": "create" #새 객체를 생성
        })),
        path("permissions/<int:pk>/", PermissionViewSet.as_view({
            "get": "retrieve", #특정 객체를 반환
            "put": "update", # 특정 객체를 수정
            "patch": "partial_update", #특정 객체를 일부 수정
            "delete": "destroy" #특정 객체 삭제
        })),
    ]
'''

'''
    TODO:
        1) 인사부 팀에 사원 등록하기.
        2) 게시판 파일 시스템 완성하기. 


'''