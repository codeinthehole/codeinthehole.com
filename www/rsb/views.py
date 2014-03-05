from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.utils import text
from tagging.models import Tag

from rsb.github import fetch_activity
from rsb.models import Article
from rsb.tweets import fetch_tweets
from . import tasks


class HomeView(TemplateView):
    template_name = 'rsb/home.html'

    def get_context_data(self):
        return {'articles': Article.objects.all().order_by('-date_published')[:5],
                'tweets': fetch_tweets(),
                'github_activity': fetch_activity('codeinthehole', num_items=8)}


class ArticleListView(ListView):
    model = Article
    template_name = 'rsb/article_list.html'
    context_object_name = 'articles'
    title = "All articles"
    popular = False

    def get_queryset(self):
        qs = self.model.objects.all().exclude(date_published=None)
        if self.popular:
            qs = qs.order_by('-num_views')
            self.title = "Popular articles"
        else:
            qs = qs.order_by('-date_published')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(ArticleListView, self).get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['feedurl'] = 'http://feeds2.feedburner.com/codeintheholecom'
        return ctx


class ArticleTagView(ListView):
    template_name = 'rsb/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['name'])
        return Article.tagged.with_all([self.tag])

    def get_context_data(self, **kwargs):
        ctx = super(ArticleTagView, self).get_context_data(**kwargs)
        ctx['title'] = self.tag.name.title()
        ctx['feedurl'] = reverse('tagged-feed', kwargs={'name': self.tag.name})
        return ctx


class ArticleFeed(Feed):

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return text.truncate_html_words(item.body_html, 120)


class AllArticlesFeed(ArticleFeed):
    title = "David Winterbottom (@codeinthehole)"
    link = "/writing/"
    description = "Latest writing"

    def items(self):
        return Article.objects.all().order_by('-date_published')[:15]


class TaggedArticlesFeed(ArticleFeed):

    def get_object(self, request, name):
        return get_object_or_404(Tag, name=name)

    def title(self, obj):
        return 'Writing on %s | David Winterbottom' % obj.name

    def link(self, obj):
        return reverse('tagged', kwargs={'name': obj.name})

    def items(self, obj):
        return Article.tagged.with_all([obj])


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'rsb/article_detail.html'
    context_object_name = 'article'

    def get(self, request, **kwargs):
        response = super(ArticleDetailView, self).get(request, **kwargs)

        # Track the view
        tasks.record_view.delay(self.object.id)

        return response

    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetailView, self).get_context_data(**kwargs)

        article = self.object
        ctx['related_articles'] = Article.tagged.related_to(article)[:6]

        # Popular articles (ignoring duples from related)
        ids_to_ignore = [a.id for a in ctx['related_articles']]
        ids_to_ignore.append(article.id)
        ctx['popular_articles'] = Article.objects.all().exclude(
            id__in=ids_to_ignore).order_by('-num_views')[:6]

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
