# config/api/router.py
from apps.core.views import CategoryViewSet

router.register(r'categories', CategoryViewSet, basename='categories')