from django.views.generic import TemplateView, DetailView, ListView
from tagging.models import Tag

from rsb.models import Article


class HomeView(TemplateView):
    template_name = 'rsb/home.html'

    def get_context_data(self):
        return {'articles': Article.objects.all().order_by('-date_created')[0:5]}
        
        
class ArticleListView(ListView):
    model = Article
    template_name = 'rsb/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        return self.model.objects.all().exclude(date_published=None)
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleListView, self).get_context_data(**kwargs)
        ctx['unpublished_articles'] = self.model.objects.filter(date_published=None)
        return ctx
    

class ArticleTagView(ListView):
    template_name = 'rsb/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        self.tag = Tag.objects.get(name=self.kwargs['name'])
        return Article.tagged.with_all([self.tag])
    
    def get_context_data(self, **kwargs):
        ctx = super(ArticleTagView, self).get_context_data(**kwargs)
        ctx['title'] = 'Articles tagged "%s"' % self.tag.name
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
        ctx['related_articles'] = Article.tagged.related_to(article)
        
        # We need to use a different date field for comparison depending on
        # if the article is published
        if article.is_published:
            previous = Article.objects.filter(date_published__lt=article.date_published)
            next = Article.objects.filter(date_published__gt=article.date_published)
        else:
            previous = Article.objects.filter(date_created__lt=article.date_created)
            next = Article.objects.filter(date_created__gt=article.date_created)
        
        ctx['previous_article'] = previous[0] if len(previous) > 0 else None
        ctx['next_article'] = next[0] if len(next) > 0 else None

        return ctx
    
class AboutView(TemplateView):
    template_name = 'about.html'


class ProjectsView(TemplateView):
    template_name = 'projects.html'

    
class TalksView(TemplateView):
    template_name = 'talks.html'
