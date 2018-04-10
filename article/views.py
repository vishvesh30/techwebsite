from django.shortcuts import render

# Create your views here.
from article.models import article_data, category_data


def article_detail(request,article_id):
    article_data_obj=article_data.objects.get(pk=article_id)
    args={
        'article_data':article_data_obj
    }
    return render(request, 'viewpost.html', args)


def getlist(request):
    article_data_obj=article_data.objects.all()
    args={
        'article_data':article_data_obj
    }
    return render(request, 'getlist.html', args)

def category_detail(request,category_id):
    article_data_obj=article_data.objects.filter(categoryid=category_id)
    category_obj=category_data.objects.get(pk=category_id)
    args = {
        'article_data': article_data_obj,
        'category_data':category_obj
    }
    return render(request, 'category_wise_list.html', args)
