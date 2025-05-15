from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES=(
        ('Not Started','Not Started'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
    )
    title=models.CharField(max_length=100)
    details=models.TextField(blank=True,null=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,default=STATUS_CHOICES[0][0])
    deadline=models.DateField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title