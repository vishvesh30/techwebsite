from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from article.models import article_data
from home.models import contact_us


def home(request):
    article_data_obj = article_data.objects.all()
    args = {
        'article_data': article_data_obj
    }
    return render(request,'home.html',args)

def contact_us_form(request):
    if request.method == 'POST':
        fname = request.POST.get('form_name')
        lname = request.POST.get('form_lastname')
        email = request.POST.get('form_email')
        message = request.POST.get('form_message')
        contact_obj = contact_us(first_name=fname, last_name=lname, email=email, message=message)
        contact_obj.save()
        return HttpResponseRedirect(reverse(contact_us_form))
    else:
        return render(request,'contact_us.html')


def about_us(request):
    return render(request,'about_us.html')