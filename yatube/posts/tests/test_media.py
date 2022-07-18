from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from ..models import Post, User, Group

User = get_user_model()


class MediaTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Daria')
        cls.group = Group.objects.create(
            title='Группа АББА',
            slug='test-slug',
            description='Дискрипшн',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст 1234',
            group=cls.group,
        )

    def setUp(self):
        self.client = Client()
