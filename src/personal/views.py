from django.shortcuts import render
from account.models import Account
from blog.models import BlogPost
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 

from blog.views import get_blog_queryset

BLOG_POSTS_PER_PAGE = 2
# Create your views here.
def home_screen_view(request):
	context = {}
	#context['some_string'] = "This is some rendom text which will be passed to template."

	# list_of_items = []
	# list_of_items.append("First entry")
	# list_of_items.append("Second entry")
	# list_of_items.append("Third entry")
	# list_of_items.append("Forth entry")

	# questions = Question.objects.all()
	# context['questions'] = questions

	# accounts = Account.objects.all()
	# context['accounts'] = accounts

	#context['list_of_items'] = list_of_items

	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	

	page = request.GET.get('page',1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts

	return render(request, "personal/home.html", context)