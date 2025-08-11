from django.contrib import admin
from django import forms
from .models import Task

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            from django.utils.text import slugify
            slug = slugify(self.cleaned_data['title'], allow_unicode=True)
        return slug


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    prepopulated_fields = {'slug': ('title',)}  # تولید خودکار از عنوان