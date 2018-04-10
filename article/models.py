from django.db import models

# Create your models here.
from author.models import author_data


class category_data(models.Model):
    category_name = models.TextField()
    category_description = models.TextField(null=True)

    def __str__(self):
        return self.category_name


class article_data(models.Model):
    authorid = models.ForeignKey(author_data, on_delete=models.DO_NOTHING)
    article_title = models.TextField()
    article_text = models.TextField()
    article_date = models.TextField()
    article_image = models.ImageField(upload_to='uploads/%Y/%m/%d',null=True)
    categoryid = models.ForeignKey(category_data, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.article_title
