# apps/tasks/tests.py
from rest_framework.test import APITestCase
from apps.accounts.models import User

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'priority': 'H'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, 201)
