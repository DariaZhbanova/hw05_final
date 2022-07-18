from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from ..models import Post, User, Group


class PostTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Daria')
        cls.group = Group.objects.create(
            title='Группа АББА',
            slug='test-slug',
            description='Дискрипшн',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def assertPost(self, post, post_b):
        self.assertEqual(post.text, post_b.text)
        self.assertEqual(post.author, post_b.author)
        self.assertEqual(post.group, post_b.group)
        self.assertEqual(post.image, post_b.image)

    def assertGroup(self, group, group_b):
        self.assertEqual(group.title, group_b.title)
        self.assertEqual(group.description, group_b.description)


class PostWithGroupAndPictureTests(PostTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст 1234',
            group=cls.group,
            image='posts/m1000x1000.jpg',
        )

    def test_index_page_show_correct_context(self):
        """При создании поста с картинкой и группой он появляется на главной"""
        response = self.authorized_client.get(reverse('posts:index'))
        first_page_object = response.context['page_obj'][0]
        self.assertPost(first_page_object, self.post)

    def test_group_page_show_correct_context(self):
        """При создании поста с картинкой и группой  он появляется на
        странице групп"""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}))
        first_page_object = response.context['page_obj'][0]
        group_object = response.context['group']
        self.assertGroup(group_object, self.group)
        self.assertPost(first_page_object, self.post)

    def test_profile_page_show_correct_context(self):
        """При создании поста с картинкой и группой он появляется в профиле"""
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': self.user.username}))
        first_page_object = response.context['page_obj'][0]
        self.assertPost(first_page_object, self.post)


class PostPagesTests(PostTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст 1234',
            image='posts/m1000x1000.jpg'
        )

    def test_post_create_page_show_correct_context_form_ields(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertFalse(response.context.get('is_edit'))

    def test_post_edit_page_show_correct_context_form_fields(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={
                'post_id': self.post.pk}))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertTrue(response.context.get('is_edit'))

    def test_post_detail_page_show_correct_context(self):
        """При создании поста с группой и картинкой он появляется
        на индивидуальной странице поста"""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}))
        self.assertPost(response.context['post'], self.post)


class PaginatorViewsTest(TestCase):
    """Тестирование пагинатора для главной, профайла и страницы групп"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        for i in range(1, 14):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Тестовый текст поста номер {i}',
                group=cls.group,
            )

    def setUp(self):
        self.some_client = Client()

    def test_index_first_page_contains_ten_records(self):
        response = self.some_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        response = self.some_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_first_page_contains_ten_records(self):
        response = self.some_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_second_page_contains_three_records(self):
        response = self.some_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_records(self):
        response = self.some_client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_three_records(self):
        response = self.some_client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)


class TemplatesTests(TestCase):
    """Проверка на использование во view-функциях правильных html-шаблонов"""
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
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_views_uses_correct_template(self):
        views_vs_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.pk}): 'posts/post_create.html'
        }
        for reverse_name, template in views_vs_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
