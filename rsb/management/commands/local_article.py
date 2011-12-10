"""
For creating a local article based on a RST file
"""
import logging
import os
import re
import datetime

from docutils.core import publish_parts
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import striptags

from rsb.models import Article
import rsb.rstcode


class Command(BaseCommand):
    args = '<path-to-article.rst>'
    output_transaction = True
    
    def handle(self, *args, **options):
        self.logger = self.create_logger() 
        if not len(args):
            raise CommandError("Please specify the article file(s) to process")
        for filepath in args:
            self.process_file(filepath)

    def process_file(self, filepath):
        self.logger.info("Processing article file %s", filepath)
        # We use the filename as the identifier of the article
        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        # Ensure filename has a 4-digit number in it
        rename_file = False
        m = re.match(r'(\d{4})-.*\.rst', filename)
        if not m:
            # New file, we need to rename
            rename_file = True
            try:
                article = Article.objects.get(filename=filename)
            except Article.DoesNotExist:
                article = Article(filename=filename)
                self.logger.info("Creating a new article")
            else:
                self.logger.info("Updating an existing article (id #%d)", article.id)
        else:
            id = int(m.group(1))
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                self.logger.warning("Creating a new article, even though the file is numbered")
                article = Article(id=id, filename=filename)
            else:
                self.logger.info("Updating an existing article (id #%d)", article.id)

        # Extract data from the RST file
        body_rst = open(filepath).read()
        parts = publish_parts(body_rst, writer_name='html4css1')

        # The subtitle should contains the summary and the tags
        sections = parts['subtitle'].split('::')
        summary = striptags(sections[0].strip())

        # Update model
        article.title = parts['title']
        article.summary = summary
        article.body_html = parts['fragment']        
        article.body_rst = body_rst
        article.date_published = datetime.datetime.now()
        article.save()
        
        if len(sections) > 1:
            article.tags = sections[1].strip()
        
        if rename_file:
            new_filename = "%04d-%s" % (article.id, filename.replace('_', '-'))
            self.logger.info("Renaming %s to %s", filename, new_filename)
            new_path = os.path.join(folder, new_filename)
            os.rename(filepath, new_path)
        
        self.logger.info("Title:   %s", article.title)
        self.logger.info("Summary: %s", article.summary)
        self.logger.info("Tags:    %s", ", ".join([tag.name for tag in article.tags.all()]))

    def create_logger(self):
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler(self.stdout))
        logger.setLevel(logging.DEBUG)
        return logger
            