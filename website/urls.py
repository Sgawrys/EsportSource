from django.conf.urls import patterns, url
from website import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login', views.loginView, name='login'),
	url(r'^logout', views.logoutView, name='logout'),
	url(r'^profile', views.profileView, name='profile'),
	url(r'^register', views.register, name='register'),
	url(r'^vote/(?P<article_id>\d+)/$', views.vote, name='vote'),
	url(r'^(?P<article_id>\d+)/$', views.article, name='article')
)