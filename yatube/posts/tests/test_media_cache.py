from django.contrib.auth import get_user_model
from django.urls import reverse
from time import sleep
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Post, Group
import shutil
import tempfile
from django.conf import settings
from ..forms import PostForm

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MediaCacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Daria')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(MediaCacheTest.user)

    def test_cache(self):
        """ Проверка работы кэширования главной страницы. """
        response_first = self.authorized_client.get(reverse('posts:index'))

        form_data = {
            'text': 'Да здравствует новый текст',
            'group': MediaCacheTest.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        sleep(2)
        response_second = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response_first.content, response_second.content)

        sleep(20 + 1)
        response_second = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(response_first.content, response_second.content)

    def test_form_create_post(self):
        """Валидная форма PostForm с картинкой создает запись в БД."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Да здравствует новый текст',
            'group': MediaCacheTest.group.pk,
            # 'pics': uploaded,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        # self.assertRedirects(response, reverse(
        #     'posts:profile',
        #     kwargs={'username': f'{ self.user.username }'}))
        self.assertEqual(response.status_code, 200)
        new_post_count = Post.objects.count()
        self.assertNotEqual(posts_count, new_post_count)
        self.assertTrue(
            Post.objects.filter(
                text='Да здравствует новый текст',
                # pics='media/small.gif',
                image='posts/small.gif',
            ).exists()
        )
