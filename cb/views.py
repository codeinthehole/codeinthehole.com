from django.views.generic import TemplateView, DetailView, ListView

from cb.models import Article


class ArticleListView(TemplateView):
    template_name = 'cb/article_list.html'

    def get_context_data(self):
        main_article = Article.objects.all().order_by('-date_created')[0]
        return {'main_article': main_article}


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'cb/article_detail.html'
    context_object_name = 'article'


class TagView(DetailView):
    template_name = 'tag.html'


class TagsView(ListView):
    template_name = 'tags.html'
