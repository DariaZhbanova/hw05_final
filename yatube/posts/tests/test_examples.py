from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Post, User, Group, Comment


User = get_user_model()


class PostWithCommentTests(TestCase):
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
            # pics='media/m1000x1000.jpg',
            image='media/m1000x1000.jpg'
        )
        # cls.comment = Comment.objects.create(
        #     post=cls.post,
        #     text_comment='Самый доброжелательный комментарий',
        # )
        cls.comment = Comment.objects.create(
            post=cls.post,
            text='Самый доброжелательный комментарий',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)


    # def test_post_detail_page_show_correct_context(self):
    #     """При создании поста с картинкой он появляется
    #     на индивидуальной странице поста"""
    #     response = self.authorized_client.get(reverse(
    #         'posts:post_detail',
    #         kwargs={'post_id': self.post.pk}))
    #     self.assertPost(response.context['post'], self.post)

    def test_post_detail_page_show_correct_context(self):
        """При создании комментария он появляется
        на индивидуальной странице поста"""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}))
        # self.assertPost(response.context['post'], self.post)
        # self.assertEqual(response.context['post'], self.post)
        self.assertEqual(response.context['comments'], self.comment)
