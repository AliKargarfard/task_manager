from rest_framework import serializers
from .models import Task
from apps.core.serializers import CategorySerializer


class TaskSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    relative_url = serializers.URLField(source="get_relative_api_url", read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id',
            'slug',
            'title',
            'image',
            'description',
            'priority',
            'deadline',
            'is_completed',
            'categories',
            'absolute_url',
            'relative_url',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('slug', 'owner', 'absolute_url', 'relative_url')
    
    # def get_absolute_url(self, obj):
    #     return obj.get_absolute_url()
    
    # def get_relative_url(self, obj):
    #     return obj.get_relative_url()

    def get_absolute_url(self, task):
        request = self.context.get("request")
        return request.build_absolute_uri(task.slug)

    def to_representation(self, instance):
        request = self.context.get("request")
        representation_data = super().to_representation(instance)
        print(request.__dict__)
        if request.parser_context.get("kwargs").get("slug"):
            representation_data.pop("snippet", None)
            representation_data.pop("absolute_url", None)
            representation_data.pop("relative_url", None)
        else:
            representation_data.pop("content", None)
        # representation_data["category"] = CategorySerializer(instance.category).data
        return representation_data