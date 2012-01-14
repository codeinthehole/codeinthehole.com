from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from tagging.models import Tag
import requests

from rsb.models import Article
from rsb.utils import fetch_tweets


class HomeView(TemplateView):
    template_name = 'rsb/home.html'

    def get_context_data(self):
        return {'articles': Article.objects.all().order_by('-date_published')[0:5],
                'tweets': fetch_tweets()}
    
        
class ArticleListView(ListView):
    model = Article
    template_name = 'rsb/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        return self.model.objects.all().exclude(date_published=None)
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleListView, self).get_context_data(**kwargs)
        ctx['title'] = "Writing"
        ctx['unpublished_articles'] = self.model.objects.filter(date_published=None)
        return ctx


class ArticlesFeedView(Feed):
    title = "David Winterbottom (@codeinthehole)"
    link = "/writing/"
    description = "Latest writing"

    def items(self):
        return Article.objects.all().order_by('-date_published')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary
    

class ArticleTagView(ListView):
    template_name = 'rsb/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['name'])
        return Article.tagged.with_all([self.tag])
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleTagView, self).get_context_data(**kwargs)
        ctx['title'] = "Writing on %s" % self.tag.name
        return ctx


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'rsb/article_detail.html'
    context_object_name = 'article'
    
    def get(self, request, **kwargs):
        response = super(ArticleDetailView, self).get(request, **kwargs)
        # Track the view
        self.object.record_view()
        return response
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetailView, self).get_context_data(**kwargs)
        
        article = self.object
        ctx['related_articles'] = Article.tagged.related_to(article)[:6]

        # Popular
        ids_to_ignore = [article.id for article in ctx['related_articles']]
        ctx['popular_articles'] = Article.objects.all().exclude(id__in=ids_to_ignore).order_by('-num_views')[:6]
        
        # We need to use a different date field for comparison depending on
        # if the article is published
        if article.is_published:
            previous_articles = Article.objects.filter(date_published__lt=article.date_published).order_by('-date_published')
            next_articles = Article.objects.filter(date_published__gt=article.date_published).order_by('date_published')
        else:
            previous_articles = Article.objects.filter(date_created__lt=article.date_created)
            next_articles = Article.objects.filter(date_created__gt=article.date_created)
        
        ctx['previous_article'] = previous_articles[0] if len(previous_articles) > 0 else None
        ctx['next_article'] = next_articles[0] if len(next_articles) > 0 else None

        return ctx
    
    
class ArticleRedirectView(RedirectView):
    """
    For ensuring SEO goodness for URLs from the old site
    """
    
    def get_redirect_url(self, **kwargs):
        try:
            article = Article.objects.get(old_id=kwargs['id'])
        except Article.DoesNotExist:
            return reverse('home')
        else:
            return article.get_absolute_url()
    
    
class AboutView(TemplateView):
    template_name = 'rsb/about.html'
