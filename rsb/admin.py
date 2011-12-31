from django.contrib import admin

from rsb.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'date_published', 'is_published', 'num_views', 'old_id')
    readonly_fields = ('num_views', 'date_updated')

admin.site.register(Article, ArticleAdmin)
