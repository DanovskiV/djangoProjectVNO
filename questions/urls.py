from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.QuestionsListView.as_view(), name='questions_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
            r'(?P<question>[-\w]+)/$',
            views.question_detail, name='question_detail'),
    url(r'^ask$', views.ask_question, name='ask')
]