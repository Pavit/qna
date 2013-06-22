from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # url(r'^$', 'questions.views.index', name='index'),
    url(r'^(?P<current_question_id>\d+)/$', 'questions.views.current_question', name='current_question'),
    url(r'^sunburstplay/$', 'questions.views.sunburstplay', name='sunburstplay'),
    url(r'^details/(?P<question_id>\d+)/', 'questions.views.question_details', name='question_details'),
    # url(r'^view/(?P<current_question_id>\d+)/$', 'questions.views.view_question', name='view_question'),
    url(r'^previous_question/(?P<previous_question_id>\d+)/$', 'questions.views.previous_question', name='previous_question'),
    url(r'^(?P<answer_id>\d+)/vote/$', 'questions.views.vote', name='vote'),
    url(r'^search/$', 'questions.views.search', name='search'),
    url(r'^search_test/$', 'questions.views.search_test', name='search_test'),
    url(r'^search_results/(?P<searchtext>\w+)/$', 'questions.views.search_results', name='search_results'),
    url(r'^submit/$', 'questions.views.submit', name='submit'),
    url(r'^search_questions/$', 'questions.views.search_questions', name='search_questions'),
    url(r'^search_answers/$', 'questions.views.search_answers', name='search_answers'),
)

urlpatterns += staticfiles_urlpatterns()