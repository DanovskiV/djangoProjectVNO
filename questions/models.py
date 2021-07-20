from django import forms
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify


class Question (models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='question_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Question, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:question_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])


class Answer(models.Model):
    answer = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    # def __str__(self):
    #     return 'Answered by {} on {}'.format(self.name, self.answer)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body')
        widgets = {'body': forms.Textarea(attrs={"type": "text",
                                                 "class": "form-group first col-sm-6 form-control",
                                                 "rows": "6",
                                                 "placeholder": "Ваш вопрос",
                                                 "label": ""}),
                   'title': forms.TextInput(attrs={"type": "text",
                                                   "class": "form-group first col-sm-6 form-control",
                                                   "placeholder": "Заголовок вопроса"})}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        # fields = ('name', 'body')
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={"type": "text",
                                                 "class": "form-control",
                                                 "rows": "5",
                                                 "placeholder": "Ваш комментарий"})}
