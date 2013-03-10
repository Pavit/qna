from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'index'),
    url(r'^(?P<current_question_id>\d+)/$', 'questions.views.current_question', name='current_question'),
    # url(r'^view/(?P<current_question_id>\d+)/$', 'questions.views.view_question', name='view_question'),
    url(r'^previous_question/(?P<previous_question_id>\d+)/$', 'questions.views.previous_question', name='previous_question'),
    url(r'^(?P<answer_id>\d+)/vote/$', 'questions.views.vote', name='vote'),
    url(r'^search/$', 'questions.views.search', name='search')
)

urlpatterns += staticfiles_urlpatterns()