from celery.task import task


@task()
def record_view(article):
    article.record_view()
