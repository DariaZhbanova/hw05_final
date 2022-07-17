from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return f'{self.title[:30]}'


class Post(models.Model):
    text_title = models.CharField(
        'Заголовок',
        max_length=200,
        blank=True,
        null=True,
        help_text='Привлеките внимание читателей самым важным')
    # pics = models.ImageField(
    #     'Картинка-волшебница',
    #     upload_to='media/',
    #     blank=True,
    #     null=True,
    #     help_text='Прикрепите картинку или фотографию',
    #     )
    image = models.ImageField(
        'Картинка-волшебница',
        upload_to='posts/',
        blank=True,
        null=True,
        help_text='Прикрепите картинку или фотографию',
        )
    text = models.TextField(
        'Текст поста',
        help_text='Поделитесь с общественностью важными новостями'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, наиболее подходящая по смыслу поста')

    @property
    def get_text_title(self):
        if self.text_title:
            return self.text_title
        return ""

    # @property
    # def get_pics(self):
    #     if self.pics:
    #         return self.pics
    #     return ""

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return f'{self.text[:15]}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост для комментирования',
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    # text_comment = models.CharField(
    #     max_length=200,
    #     null=True,
    #     verbose_name='Ваш комментарий',
    #     help_text='Напишите Ваши впечатления после прочтения поста',
    # )
    text = models.TextField(
        max_length=200,
        null=True,
        verbose_name='Ваш комментарий',
        help_text='Напишите Ваши впечатления после прочтения поста',
    )
    created = models.DateTimeField(
        'Дата комментирования',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']

    # def __str__(self) -> str:
    #     return self.text_comment[:15]
    def __str__(self) -> str:
        return self.text[:15]

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=None,
        verbose_name='Читающий',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Читаемый',
        related_name='following',
    )

    def __str__(self):
        return f"Читающий: '{self.user}', Читаемый: '{self.author}'"