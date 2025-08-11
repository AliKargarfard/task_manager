from django.db import models
from slugify import slugify
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

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
    image = models.ImageField(
        upload_to='tasks/images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        verbose_name="تصویر تسک"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-\w]+$',
                message=_('Enter a valid "slug" with letters, numbers, underscores or hyphens.'),
                code='invalid_slug'
            )
        ],
        allow_unicode=True,  # فعال‌سازی پشتیبانی از یونیکد (فارسی)
    )
    # slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # استفاده از نسخه پیشرفته slugify با پشتیبانی فارسی
            self.slug = slugify(
                self.title,
                max_length=200,
                word_boundary=True,
                save_order=True,
                allow_unicode=True  # حیاتی برای فارسی
            )
            
            # اگر هنوز خالی بود
            if not self.slug:
                import uuid
                self.slug = f'task-{uuid.uuid4().hex[:8]}'
                
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('task-detail', kwargs={'slug': self.slug})
    
    def get_relative_url(self):
        return f'/api/tasks/{self.slug}/'
    
    def get_relative_api_url(self):
        return reverse("task-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return f"{self.title} - {self.get_priority_display()}"