"""
For creating a local article based on a RST file
"""
import logging
import os
from docutils.core import publish_parts

from django.core.management.base import BaseCommand, CommandError

from cb.models import Article


class Command(BaseCommand):
    args = '<path-to-article.rst>'
    output_transaction = True
    
    def handle(self, *args, **options):
        logger = self.create_logger() 
        if len(args) != 1:
            raise CommandError("Please specify the article file to process")
        logger.info("Processing article file %s", args[0])

        # We use the filename as the identifier of the article
        filepath = args[0]
        filename = os.path.basename(filepath)
        try:
            article = Article.objects.get(filename=filename)
        except Article.DoesNotExist:
            article = Article(filename=filename)
            logger.info("Creating a new article")
        else:
            logger.info("Updating an existing article (id #%d)", article.id)

        # Extract data from the RST file
        body_rst = open(filepath).read()
        parts = publish_parts(body_rst, writer_name='html4css1')

        # Update model
        article.title = parts['title']
        article.body_html = parts['fragment']        
        article.body_rst = body_rst
        article.save()
        
        logger.info("Title: %s", article.title)

    def create_logger(self):
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler(self.stdout))
        logger.setLevel(logging.DEBUG)
        return logger
            