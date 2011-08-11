from django.views.generic import TemplateView, DetailView, ListView

from cb.models import Article


class ArticleListView(TemplateView):
    template_name = 'cb/article-list.html'

    def get_context_data(self):
        main_article = Article.objects.all().order_by('-date_created')[0]
        return {'main_article': main_article}


class ArticleView(DetailView):
    template_name = 'article.html'


class TagView(DetailView):
    template_name = 'tag.html'


class TagsView(ListView):
    template_name = 'tags.html'
