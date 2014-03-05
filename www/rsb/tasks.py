from celery.task import task

from . import models


@task()
def record_view(article_id):
    try:
        article = models.Article.objects.get(id=article_id)
    except models.Article.DoesNotExist:
        pass
    else:
        print "Updating count for article #%s" % article.id
        article.record_view()
