from django.db import models

class Post(models.Model):

    author = models.TextField(max_length=30,
                              verbose_name='Автор')
    name = models.CharField(max_length=40,
                            verbose_name='Название поста')
    description = models.TextField(max_length=300,
                                   verbose_name='Описание поста',
                                   null=True,
                                   blank=True)
    url = models.URLField(null=True,
                          verbose_name='Ссылка на инструкцию',
                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.name
