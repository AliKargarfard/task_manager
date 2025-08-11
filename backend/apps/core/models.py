from django.db import models
from apps.accounts.models import User

class BaseModel(models.Model):
    """
    مدل پایه با فیلدهای مشترک تمام مدل‌ها
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    class Meta:
        abstract = True  # این مدل به صورت مستقل در دیتابیس ایجاد نمی‌شود
        ordering = ['-created_at']

class Category(BaseModel):
    """
    مدل دسته‌بندی مشترک بین تمام اپلیکیشن‌ها
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    color = models.CharField(max_length=7, default='#808080', verbose_name="کد رنگ")
    icon = models.ImageField(
        upload_to='categories/icons/',
        blank=True,
        verbose_name="آیکون",
        help_text="آیکون دسته‌بندی با فرمت SVG یا PNG"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="مالک"
    )

    class Meta(BaseModel.Meta):
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)