from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateTimeField('date published')
	content = models.CharField(max_length=10000)
	author = models.ForeignKey(User, unique=False)
	game_id = models.IntegerField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)

class AuthorInfo(models.Model):
	user = models.OneToOneField(User)
	blurb = models.CharField(max_length=140)
	fb_link = models.CharField(max_length=200, blank=True)
	twitter_link = models.CharField(max_length=200, blank=True)
	github_link = models.CharField(max_length=200, blank=True)
	email = models.CharField(max_length=200, blank=True)
	instagram_link = models.CharField(max_length=200, blank=True)
	image = models.ImageField(upload_to='img')