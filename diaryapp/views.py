from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserModel
import bs4
import requests


# Create your views here.

def landing_page(request):
    return render(request, "landing_page.html")


def signup(request):
    if request.method == "POST":
        n = request.POST.get("name")
        e = request.POST.get("email")
        p = request.POST.get("password")
        g = request.POST.get("gender")
        print(n, e, p, g)
        try:
            user = UserModel.objects.create(
                email=e, name=n, password=p, gender=g)
            print('user.......', user)
            user.save()
            return HttpResponse("successful")

        except:
            return HttpResponse("failed")
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == "POST":

        e = request.POST.get("email")
        p = request.POST.get("password")

        if e == '' or p == '':
            HttpResponse('Please enter your email and password')
            return redirect('login')

        else:

            print(e, p)
            try:
                user = UserModel.objects.filter(email=e, password=p)

                if user.count() > 0:
                    for user in user:
                        request.session['email'] = user.email
                        request.session['id'] = user.id
                        request.session['name'] = user.name
                        return redirect('home')
                else:
                    return HttpResponse('successful')
            except:
                return HttpResponse("failed")
    else:
        return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def blog(request):
    # mental health news and blog : mq
    url1 = 'https://www.mqmentalhealth.org/news-blog'
    page = requests.get(url1)
    soup1 = bs4.BeautifulSoup(page.content, 'html5lib')
    article = soup1.findAll('article')

    dict1 = {}

    for x in article:
        dict = {}
        print()
        try:
            a = x.find('header').get_text()
            dict['href'] = (x.find('a'))['href']
            dict['imgsrc'] = (x.find('img'))['src']
            dict['title'] = x.find('header').get_text()
            dict['author'] = x.find('footer').find('a').get_text()
            dict['desc'] = x.find('p').get_text()
            dict['date'] = x.find('time').get_text()

            print()
            print(dict)
            dict1[a] = (dict)
        except:
            pass

    # story blogs about mental health
    url1 = 'https://www.blurtitout.org/blog/'
    page = requests.get(url1)
    soup1 = bs4.BeautifulSoup(page.content, 'html5lib')
    article = soup1.findAll("article")

    dict2 = {}
    for x in article:
        dict = {}
        print()
        try:
            a = x.find('header').get_text()
            dict['href'] = (x.find('a'))['href']
            dict['imgsrc'] = (x.find('img'))['src']
            dict['title'] = x.find('h1').get_text()
            dict['author'] = "Blurt Team"
            dict['desc'] = x.find('section').find('p').string
            dict['date'] = x.find('time').get_text()

            print()
            print(dict)
            dict2[a] = (dict)
        except:
            pass

    return render(request, 'blog.html', {'mq': dict1, 'rethink': dict2})


def diary(request):
    return render(request, 'diary.html')


def logout(request):
    request.session.flush()
    return redirect('landingpage')
