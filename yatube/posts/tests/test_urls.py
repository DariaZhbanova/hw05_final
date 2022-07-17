from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group, User

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        example = Post.objects.create(
            author=self.user,
            text='Some user\'s authorized text')
        templates_url_names = {
            '/': 'posts/index.html',
            (f'/group/{ self.group.slug }/'): 'posts/group_list.html',
            (f'/profile/{ self.post.author.username }/'):
            'posts/profile.html',
            (f'/posts/{ example.pk }/'): 'posts/post_detail.html',
            (f'/posts/{ example.pk }/edit/'): 'posts/post_create.html',
            '/create/': 'posts/post_create.html',
        }

        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_unexisting_url(self):
        """Проверка доступности адреса несуществующей стр."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_url_exists_at_desired_location(self):
        """Проверка доступности адреса создания поста для гостя и
        редирект на страницу авторизации."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_pages_for_guest(self):
        """Проверка доступности страниц для неавторизованных посетителей."""
        templates_url_names_guest = {
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.post.author.username}/',
        }
        for address in templates_url_names_guest:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_authorized(self):
        """Проверка доступности страниц для авторизованных пользователей."""
        templates_url_names_authorized = {
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.post.author.username}/',
            f'/posts/{self.post.pk}/',
            '/create/',
        }
        for address in templates_url_names_authorized:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_author(self):
        """Проверка доступности страниц только для автора."""
        example = Post.objects.create(
            author=self.user,
            text='Some author\'s text')
        templates_url_names_author = {
            f'/posts/{example.pk}/edit/',
        }
        for address in templates_url_names_author:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
