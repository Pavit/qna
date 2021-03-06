from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'questions.views.index', name='index'),
    url(r'^profile/$', 'questions.views.profile', name='profile'),
    url(r'', include('social_auth.urls')),
    # url(r'^qna/', include('qna.foo.urls')),
    url(r'^questions/', include('questions.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook_login_success/$', 'questions.views.facebook_login_success'),
    url(r'^logout/$', 'core.views.logout_view', name='logout'),
    url(r'^typeahead_test.html/$', 'questions.views.typeahead_test', name='typeahead_test'),
)
