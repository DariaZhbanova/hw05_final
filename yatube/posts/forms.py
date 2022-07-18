from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = {'text', 'image', 'group'}
        labels = {
            'text': 'Введите текст:',
            'group': 'Выберите группу:'
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = {'text'}
        labels = {
            'text': 'Комментарий',
        }
