# board/models.py
from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "board"
        
    def __str__(self):
        return self.title
    
class File(models.Model):
    board = models.ForeignKey('Board', related_name='files', on_delete=models.CASCADE)  # 게시글과 파일의 관계
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')  # 파일 경로
    name = models.CharField(max_length=255)  # 파일 이름
    file_size = models.PositiveIntegerField()  # 파일 크기 (바이트 단위)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 파일 업로드 시간
    updated_at = models.DateTimeField(auto_now=True)  # 파일 수정 시간
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 업로드한 사용자
    file_type = models.CharField(max_length=50, blank=True, null=True)  # 파일 유형 (예: 'image', 'pdf', 등)
    is_processed = models.BooleanField(default=False)  # 파일 처리 상태 (예: PDF 변환, 압축 등)
    is_encrypted = models.BooleanField(default=False)  # 파일 암호화 여부
    status = models.CharField(
        max_length=20,
        choices=[('uploaded', 'Uploaded'), ('processing', 'Processing'), ('completed', 'Completed')],
        default='uploaded'
    )  # 파일 상태 (업로드, 처리 중, 완료 등)
    description = models.TextField(blank=True, null=True)  # 파일에 대한 설명

    class Meta:
        db_table = 'files'

    def __str__(self):
        return self.name