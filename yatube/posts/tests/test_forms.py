from django.test import TestCase, Client
from ..models import Post, Group, User
from django.urls import reverse
from ..forms import PostForm


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Daria')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_form_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Да здравствует новый текст',
            'group': PostFormTest.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': f'{ self.user.username }'}))
        new_post_count = Post.objects.count()
        last_post = Post.objects.last()

        self.assertNotEqual(posts_count, new_post_count)
        self.assertEqual(last_post.text, form_data['text'])
        self.assertEqual(last_post.group.pk, form_data['group'])

    def test_form_edit_post(self):
        """Валидная форма редактирует запись в БД."""
        example = Post.objects.create(
            author=self.user,
            text='Some author\'s text', )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст 123',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{ example.pk }'}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': f'{ example.pk }'}))
        after_edit_count = Post.objects.count()

        self.assertEqual(posts_count, after_edit_count)
        self.assertNotEqual(f'{ example.text }', form_data['text'])


class CreationFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.form_data = {
            'first_name': 'Mark',
            'last_name': 'Brodskiy',
            'username': 'markmark',
            'email': 'smthng@mail.ru',
            'password1': '@Kuku6928',
            'password2': '@Kuku6928',
        }

    def setUp(self):
        self.guest_client = Client()

    def test_new_user(self):
        """Валидная форма создает запись в БД."""
        users_count = User.objects.count()
        response = self.guest_client.post(
            reverse('users:signup'),
            data=self.form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse('posts:index'))
        new_users_count = User.objects.count()
        self.assertNotEqual(users_count, new_users_count)
