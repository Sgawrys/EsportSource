from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import RequestContext, loader
from website.models import Article, AuthorInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from pagedown.widgets import PagedownWidget
import datetime

'''
	Form for writing an article and describing what game universe
	the article is a part of.
'''
class ArticleForm(forms.Form):
	game_options = (('0', 'League of Legends'),
					('1', 'Counter-Strike: Global Offensive'),
					('2', 'Dota 2'),
					('3', 'Hearthstone'),
					('4', 'Heroes of the Storm'),
					('5', 'Smite'),
					('6', 'Starcraft II'))

	title = forms.CharField(label='Title', max_length=200)
	content = forms.CharField(widget=PagedownWidget())
	game_id = forms.ChoiceField(label = 'Game',widget=forms.Select, choices=game_options)

'''
	Form for authenticating users, needs registration form still.
'''
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:150px'}), label='Username', max_length=16)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'style':'width:150px'}))

'''
	Form for registering a new user account on the website.
'''
class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(), label='Username', max_length=16)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	email = forms.EmailField()

'''
	Form that allows users to change their personal information that
	is displayed on articles written by those respective users.
'''
class ProfileForm(forms.Form):
	first_name = forms.CharField(label='First Name', max_length=64)
	last_name = forms.CharField(label='Last Name', max_length=64)
	blurb = forms.CharField(label='Blurb', max_length=256, widget=forms.Textarea)
	fb_link = forms.CharField(label='Facebook', max_length=128)
	twitter_link = forms.CharField(label='Twitter', max_length=128)
	github_link = forms.CharField(label='Github', max_length=128)
	instagram_link = forms.CharField(label='Instagram', max_length=128)
	email = forms.CharField(label='Email', max_length=128)
	image_link = forms.ImageField(label='Picture', max_length=128, required=False)

'''
	Home page, displays latest articles and allows users to
	write their own articles.
'''
def index(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			createArticle(request, form).save()
	article_form = ArticleForm()
	articles = Article.objects.all()[:5]
	template = loader.get_template('index.html')
	login_form = LoginForm()
	register_form = RegisterForm()
	context = RequestContext(request, {
		'articles' : articles,
		'form' : article_form,
		'login' : login_form,
		'register' : register_form
		})
	return HttpResponse(template.render(context))

'''
	Finds the article in the database based on the article_id,
	returns the template responsible for displaying the desired
	information.
'''
def article(request, article_id):
	article = Article.objects.get(id=article_id)
	author_info = AuthorInfo.objects.get(user=article.author)
	template = loader.get_template('template.html')
	context = RequestContext(request, {
		'article' : article,
		'author_info' : author_info
		})
	return HttpResponse(template.render(context))

'''
	Responsible for the logging in of users and returns them
	back to the home page.
'''
def loginView(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username = form.cleaned_data['username'],
				password = form.cleaned_data['password'])
			if user is not None:
				login(request, user)
				return redirect('index')
			else:
				return redirect('index')
'''
	Logs the user out and returns them to the home page.
'''
def logoutView(request):
	logout(request)
	return redirect('index')

'''
	Creates an article based on form data gathered from a user
	writing a story on the home page.
'''
def createArticle(request, valid_form):
	new_article = Article(title = valid_form.cleaned_data['title'], 
		content = valid_form.cleaned_data['content'], 
		game_id = valid_form.cleaned_data['game_id'], 
		author = request.user, 
		date = datetime.datetime.now())
	return new_article

'''
	Allows users to vote on certain written articles, has to be updated
	to only allow one vote per article per user.
'''
def vote(request, article_id):
	if request.method == 'POST':
		article = Article.objects.get(id=article_id)
		if request.POST['vote'] == '1':
			article.upvotes += 1
		else:
			article.downvotes += 1
		article.save()
		return JsonResponse({"upvotes" : article.upvotes, "downvotes" : article.downvotes})
	return HttpResponseNotFound()

'''
	Allows users to change their associated information that would show up on
	published articles, if a field isn't set it will continue to be whatever
	the user previously entered.
'''
def profileView(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			current_user = User.objects.get(username = request.user.username)
			current_user.first_name = form.cleaned_data['first_name']
			current_user.last_name = form.cleaned_data['last_name']
			author_info = AuthorInfo.objects.get(user=current_user)
			author_info.blurb = form.cleaned_data['blurb']
			author_info.fb_link = form.cleaned_data['fb_link']
			author_info.twitter_link = form.cleaned_data['twitter_link']
			author_info.github_link = form.cleaned_data['github_link']
			author_info.email = form.cleaned_data['email']
			author_info.instagram_link = form.cleaned_data['instagram_link']
			author_info.image = form.cleaned_data['image_link']		
			current_user.save()
			author_info.save()
		else:
			print "Form is not valid"
			print form.errors
	profileForm = ProfileForm()
	template = loader.get_template('profile.html')
	context = RequestContext(request, {
		'user' : request.user,
		'profile' : profileForm
		})
	return HttpResponse(template.render(context))

'''
	Allows submittal of registration form for purposes of new user account
	creation.
'''
def register(request):
	#Send e-mail about registration to click link
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'], last_login = datetime.datetime.now())
			user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
			if user is not None:
				login(request, user)
			new_user.save()
	return redirect('profile')