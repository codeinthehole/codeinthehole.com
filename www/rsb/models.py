import tagging
import datetime
import math

from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


class Article(models.Model):

    # This is used to identify the article
    filename = models.CharField(max_length=255, unique=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.TextField()

    # Article is created in RST, oonverted to HTML
    body_rst = models.TextField()
    body_html = models.TextField()

    # Track number of clicks
    num_views = models.PositiveIntegerField(default=0, db_index=True)

    date_created = models.DateTimeField(auto_now_add=True)

    # This is the date the article was uploaded from the dev
    # environment to production.  That is what "published" means.
    date_published = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)

    # The ID from the old blogging software to allow redirects
    old_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-date_published',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    @property
    def is_published(self):
        return self.date_published is not None

    @property
    def age(self):
        now = datetime.datetime.now()
        return now - self.date_published

    @property
    def age_in_years(self):
        return int(math.floor(self.age.days / 365))

    @property
    def is_old(self):
        return self.age_in_years >= 2

    def record_view(self):
        self.num_views += 1
        self.save()


tagging.register(Article)
