from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus
from ..models import Comment, User, Post


class CommentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Daria')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст 1234',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_detail_page_show_correct_comment(self):
        """При добавлении комментария от
        неавторизованного пользователя он не будет добавлен в БД,
        а сам гость редиректится на страницу авторизации
        и оттуда к комментированию поста.
        При создании коммента от авторизованного пользователя
        в БД появляется +1 запись,
        а сам комментарий отображается на индивидуальной
        странице поста."""
        comments_count = Comment.objects.count()
        form_data = {
            'author': self.user,
            'post': self.post,
            'text': 'Самый доброжелательный комментарий',
        }
        response_one = self.guest_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': self.post.pk}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response_one,
            f'/auth/login/?next=/posts/{self.post.pk}/comment/')
        guest_comments_count = Comment.objects.count()
        self.assertEqual(comments_count, guest_comments_count)
        self.assertEqual(response_one.status_code, HTTPStatus.OK)

        response_two = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': self.post.pk}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response_two, reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}))
        new_comments_count = Comment.objects.count()
        self.assertNotEqual(comments_count, new_comments_count)

        last_comment = Comment.objects.last()
        response_three = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.pk}))
        self.assertEqual(response_three.context['comments'][0], last_comment)
