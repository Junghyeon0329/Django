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
    board = models.ForeignKey(Board, related_name='files', on_delete=models.CASCADE)  # 게시글과 관계
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')  # 파일 저장 경로
    name = models.CharField(max_length=255)  # 파일 이름
    file_size = models.PositiveIntegerField()  # 파일 크기 (바이트 단위)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 파일 업로드 일시
    
    class Meta:
        db_table = "board_files"
    
    def __str__(self):
        return self.name