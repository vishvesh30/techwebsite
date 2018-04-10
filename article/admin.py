from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

from article.models import article_data

class article_data_admin(SummernoteModelAdmin):
    summernote_fields = ('article_text')


admin.site.register(article_data,article_data_admin)