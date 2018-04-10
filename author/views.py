import datetime
import os
import random
import uuid

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from article.models import article_data, category_data
from author.forms import insertarticleForm, updatearticleForm
from author.models import author_data, otp_generator

# Create your views here.
from techwebsite import settings


def insertarticle(request):
    form = insertarticleForm()
    if 'authorid' in request.session:
        category_obj = category_data.objects.all()
        if request.method == 'POST':
            title = request.POST.get('title')
            data = request.POST.get('article_text')
            date = datetime.datetime.now().date()
            myfile = request.FILES['article_image']
            author_obj = author_data.objects.get(pk=request.session['authorid'])
            category_obj1 = category_data.objects.get(pk=request.POST.get('categoryid'))
            article_obj = article_data(article_title=title, article_text=data, article_date=date, authorid=author_obj,
                                       categoryid=category_obj1, article_image=myfile)
            article_obj.save()
            args = {
                'form': form,
                'message': 'Article saved Successfully',
                'category_obj': category_obj
            }
            return render(request, 'insertform.html', args)

        else:
            args = {
                'form': form,
                'category_obj': category_obj
            }
            return render(request, 'insertform.html', args)
    else:
        return HttpResponseRedirect('/author/login/')


def login(request):
    if 'authorid' in request.session:
        return HttpResponseRedirect('/author/dashboard/')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            pwd = request.POST.get('password')
            try:
                author_data_obj = author_data.objects.get(author_email=email)
                if author_data_obj.author_password == pwd:
                    request.session['authorid'] = author_data_obj.pk
                    return HttpResponseRedirect('/author/dashboard/')
                else:
                    args = {
                        'message': 'Email or Password incorrect'
                    }
                    return render(request, 'login.html', args)
            except Exception as e:
                print(e)
                args = {
                    'message': 'Email doesnot exist'
                }
                return render(request, 'login.html', args)
        else:
            return render(request, 'login.html')


def dashboard(request):
    if 'authorid' in request.session:
        obj = author_data.objects.get(pk=request.session['authorid'])
        author_articles = article_data.objects.filter(authorid_id=request.session['authorid'])
        args = {
            'author_data': obj,
            'article_data': author_articles
        }
        return render(request, 'dashboard.html', args)
    else:

        return HttpResponseRedirect('/author/login/')


def update_personal_info(request):
    if 'authorid' in request.session:
        author_obj = author_data.objects.get(pk=request.session['authorid'])

        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            myfile = request.FILES['img']
            # for future last update date use
            author_obj.author_fname = fname
            author_obj.author_lname = lname
            author_obj.author_email = email
            author_obj.author_img = myfile
            author_obj.save()
            args = {
                'author_data': author_obj,
                'message': 'Article saved Successfully'
            }
            return render(request, 'updatepersonalinfo.html', args)
        else:
            args = {
                'author_data': author_obj,
            }
            return render(request, 'updatepersonalinfo.html', args)
    else:

        return HttpResponseRedirect('/author/login/')


def logout(request):
    if 'authorid' in request.session:
        del request.session['authorid']
    return HttpResponseRedirect('/author/login/')


def view_author(request, author_id):
    article_data_author = article_data.objects.filter(authorid=author_id)
    author_data_obj = author_data.objects.get(pk=author_id)
    args = {
        'article_data': article_data_author,
        'author_data': author_data_obj
    }
    return render(request, 'viewauthor.html', args)


def update_article(request, article_id):
    if 'authorid' in request.session:
        category_obj = category_data.objects.all()
        article_obj = article_data.objects.get(pk=article_id)
        if article_obj.authorid_id == request.session['authorid']:
            if request.method == 'POST':
                title = request.POST.get('title')
                data = request.POST.get('data')
                if request.FILES:
                    print(request.FILES)
                    myfile = request.FILES['article_image']
                    article_obj.article_image = myfile
                # for future last update date use
                date = datetime.datetime.now().date()
                article_obj.article_title = title
                article_obj.article_text = data

                category_obj1 = category_data.objects.get(pk=request.POST.get('categoryid'))
                article_obj.categoryid = category_obj1
                article_obj.save()
                args = {
                    'article_data': article_obj,
                    'message': 'Article saved Successfully',
                    'category_obj': category_obj
                }
                return render(request, 'updateform.html', args)

            else:
                args = {
                    'category_obj': category_obj,
                    'article_data': article_obj
                }
                return render(request, 'updateform.html', args)
        else:
            # if there is one author who tries to chnange another authoer's article using article's primarykey
            return HttpResponseRedirect('/author/dashboard/')
    else:
        return HttpResponseRedirect('/author/login/')


def forgotpassword(request):
    if 'authorid' in request.session:
        return HttpResponseRedirect('/author/dashboard/')
    elif request.method == 'POST':
        email = request.POST.get('email')
        try:
            author_obj = author_data.objects.get(author_email=email)
        except:
            args = {
                'message': 'Email id doesnot Exist'
            }
            return render(request, 'forgotpassword.html', args)
        otp_str = ''
        for i in range(6):

            if random.choice('01') == '0':
                otp_str += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            else:
                otp_str += random.choice('0123456789')
        send_mail(
            subject='Your OTP for Techwebsite',
            from_email='rajvikapadia2602@gmail.com',
            recipient_list=[author_obj.author_email],
            fail_silently=False,
            message="Otpbfhjyjhgk" + otp_str,
            html_message='<html><body><h1>Your OTP is : ' + otp_str + '</h1></body></html>',
        )
        otp_generator.objects.filter(author_id=author_obj).delete()
        otp_data = otp_generator(author_id=author_obj, otp=otp_str)
        otp_data.save()

        return HttpResponseRedirect('/author/verifyotp/' + str(author_obj.pk) + '/')
    else:
        return render(request, 'forgotpassword.html')


def verifyotp(request, author_id):
    author_data_obj = author_data.objects.get(pk=author_id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_obj = otp_generator.objects.get(author_id=author_data_obj)
        if otp_obj.otp == otp:
            otp_generator.objects.filter(author_id=author_data_obj).delete()

            return HttpResponseRedirect('/author/setpassword/' + str(author_data_obj.pk) + '/')
        else:
            args = {
                'message': 'OTP you entered is Wrong',
                'author_data': author_data_obj
            }

            return render(request, 'verifyotp.html', args)
    else:
        args = {
            'author_data': author_data_obj
        }
        return render(request, 'verifyotp.html', args)


def setpassword(request, author_id):
    author_data_obj = author_data.objects.get(pk=author_id)
    if request.method == 'POST':
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('repassword')
        if pass1 == pass2:
            author_data.objects.filter(pk=author_id).update(author_password=pass1)
            request.session['authorid'] = author_data_obj.pk
            return HttpResponseRedirect('/author/dashboard/')
        else:
            args = {
                'message': 'Password and Retype Password are not matched !!',
                'author_data': author_data_obj
            }
            return render(request, 'setpassword.html', args)
    else:
        args = {
            'author_data': author_data_obj
        }
        return render(request, 'setpassword.html', args)


def register(request):
    if 'authorid' in request.session:
        return HttpResponseRedirect('/author/dashboard/')
    else:
        if request.method == 'POST' and request.FILES:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            myfile = request.FILES['img']
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('repassword')
            curr_date = datetime.datetime.now().date()
            try:
                check_obj = author_data.objects.get(author_email=email)

                args = {
                    'message': 'Email already exists'
                }
                return render(request, 'register.html', args)
            except Exception as e:
                if pass1 == pass2:
                    author_data_obj = author_data(author_fname=fname, author_lname=lname, author_email=email,
                                                  author_password=pass1, author_img=myfile, author_joined=curr_date)
                    author_data_obj.save()
                    request.session['authorid'] = author_data_obj.pk
                    return HttpResponseRedirect('/author/dashboard/')
                else:
                    args = {
                        'message': 'Password and Retype Password Doesnot Match'
                    }
                    return render(request, 'register.html', args)

        else:
            return render(request, 'register.html')
