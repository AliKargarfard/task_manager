from django.db import models
from apps.core.models import BaseModel, Category
from apps.accounts.models import User


class Task(BaseModel):
    """مدل اصلی وظایف"""
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    deadline = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.title} - {self.get_priority_display()}"