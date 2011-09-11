from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


class Article(models.Model):
    """
    Blog article
    """
    
    # This is used to identify the article
    filename = models.CharField(max_length=255, unique=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.TextField()
    
    # Article is created in RST, oonverted to HTML
    body_rst = models.TextField()
    body_html = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    
    # This is the date the article was uploaded from the dev 
    # environment to production.  That is what "published" means.
    date_published = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)

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

