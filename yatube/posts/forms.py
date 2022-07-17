from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post
        # fields = {'text_title', 'text', 'pics', 'group'}
        # fields = {'text_title', 'text', 'image', 'group'}
        fields = {'text', 'image', 'group'}
        labels = {
            'text_title': 'Заголовок',
            'text': 'Введите текст:',
            'group': 'Выберите группу:'
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        # fields = {'text_comment'}
        fields = {'text'}
        labels = {
            # 'text_comment': 'Комментарий',
            'text': 'Комментарий',
        }
