from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserModel, DiaryModel
import bs4
import requests
from textblob import TextBlob, classifiers
import itertools
import time
import random

from sentiment import predict

# Create your views here.

# movie recommendation
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP

# Main Function for scraping


def main(emotion):

    # IMDb Url for Drama genre of
    # movie against emotion Sad
    if(emotion == -1):
        urlhere = 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Thriller genre of
    # movie against emotion Enjoyment
    elif(emotion == 1):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Film_noir genre of
    # movie against emotion Surprise
    elif(emotion == 0):
        urlhere = 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter, asc'

    # HTTP request to get the data of
    # the whole page
    try:
        page = requests.get(urlhere)
        soup = bs4.BeautifulSoup(page.content, "html5lib")
        # Parsing the data using
        # BeautifulSoup
        a = soup.findAll("div", {'class': 'lister-item mode-advanced'})
        # Extract movie titles from the
        # data using regex
        movies = {}
        for x in a:
            inmovie = {}
            # imgsrc = (x.find('img'))['src']
            movie = x.find('h3', {'class': 'lister-item-header'}
                           ).find('a').get_text()
            desc = (x.findAll('p'))[1].get_text()
            inmovie['name'] = movie
            inmovie['desc'] = desc
            # inmovie['imgsrc'] = imgsrc
            movies[movie] = inmovie

        keys = list(movies.keys())
        random.shuffle(keys)
        moviesh = {}

        for key in keys:
            moviesh.update({key: movies[key]})

        return moviesh
    except:
        pass


def mainmovie(emotion):
    if(emotion == -1):
        url = "https://www.buzzfeed.com/cieravelarde/harry-potter-is-truly-magical"
        # IMDb Url for Thriller genre of
        # movie against emotion Enjoyment
    elif(emotion == 1):
        url = "https://www.buzzfeed.com/lincolnthompson/31-of-the-most-heartwarming-books-youll-ever-read"
    # IMDb Url for Film_noir genre of
    # movie against emotion Surprise
    elif(emotion == 0):
        url = "https://www.buzzfeed.com/hilarywardle/fascinating-books-everyone-needs-to-own"

    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html5lib")
    div = soup.find_all('span', {'class': 'js-subbuzz__title-text'})

    book = {}
    count = 0
    for x in div:
        if count > 0:
            name = x.get_text()
            book[count] = name

        count += 1

    keys = list(book.keys())
    random.shuffle(keys)
    booksh = {}

    for key in keys:
        booksh.update({key: book[key]})

    return booksh


def mainpodcasts(emotion):
    print("inside the function def")
    if(emotion == -1):
        url = "https://www.bustle.com/p/12-podcasts-to-help-anxiety-depression-whether-you-want-to-laugh-cry-find-a-way-to-unwind-15909570"
        # IMDb Url for Thriller genre of
        # movie against emotion Enjoyment
    elif(emotion == 1):
        url = "https://www.bustle.com/p/9-podcasts-for-positivity-that-will-brighten-up-your-day-80391"
    # IMDb Url for Film_noir genre of
    # movie against emotion Surprise
    elif(emotion == 0):
        url = "https://www.bustle.com/p/19-motivating-podcasts-to-help-you-start-2020-on-the-right-foot-19421406"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html5lib")
    div = soup.find_all('h3', {'class': 'jf'})
    print(div)

    podcast = {}
    count = 1
    for title in div:
        #     title=x.find('h3',{'class':'jh'})
        title = title.get_text()
        title = title[3:]
        podcast[count] = title
        count += 1
    print(podcast)

    keys = list(podcast.keys())
    random.shuffle(keys)
    podcasts = {}

    for key in keys:
        podcasts.update({key: podcast[key]})

    return podcast


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
            return redirect(login)

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
                        request.session['gender'] = user.gender
                        return redirect('home')
                else:
                    return render(request, 'login.html')
            except:
                return HttpResponse("failed")
    else:
        return render(request, 'login.html')


def home(request):
    # try:
    if (DiaryModel.objects.filter(user=request.session['id'])).count() > 0:
        diary = DiaryModel.objects.filter(
            user=request.session['id']).order_by("-id")[0]
        pol = diary.polarity
    else:
        pol = 0
    a = main(pol)
    b = mainmovie(pol)
    c = mainpodcasts(pol)

    movie = dict(itertools.islice(a.items(), 6))
    book = dict(itertools.islice(b.items(), 6))
    podcast = dict(itertools.islice(c.items(), 6))

    # return render(request, 'home.html', out)

    # return HttpResponse(c)
    return render(request, 'home.html', {'movies': movie, 'podcasts': podcast, 'books': book})

    # except:
    # return HttpResponse('failed')

    #  return render(request, 'home.html')


def blog(request):
    # mental health news and blog : mq
    try:
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

    except:
        return HttpResponse("This requires internet connection. Please make sure you are connected to internet")


def diary(request):
    if request.method == "POST":
        diary = request.POST.get("diary")
        usern = request.POST.get("name")
        print(diary)

        try:
            print('predict----->', predict(diary))
            sentim = predict(diary)

        except:
            pass
        sentimentp = TextBlob(diary).sentiment.polarity
        if(sentimentp < 0):
            sentimentp = -1
        elif(sentimentp > 0):
            sentimentp = 1
        else:
            sentimentp = 0

        try:
            usern = UserModel.objects.get(id=usern)
            userdiary = DiaryModel.objects.create(
                description=diary, polarity=sentimentp, user=usern)
            userdiary.save()
            return redirect("home")
        except:
            return HttpResponse("failed")

    else:
        return render(request, 'diary.html')


def logout(request):
    request.session.flush()
    return redirect('landingpage')


def profile(request):
    if request.method == "POST":
        n = request.POST.get("name")
        e = request.POST.get("email")
        g = request.POST.get("gender")
        try:
            if g != 'Male' or g != 'Female':
                g = request.session["gender"]

            print(n, e, g)
            user = UserModel.objects.filter(id=request.session['id'])

            print('user.......', user)
            user.update(name=n, email=e, gender=g)
            time.sleep(1)
            HttpResponse('Please login to see changes')
            time.sleep(2)
            return render(request, 'login.html')
        except:
            return HttpResponse("failed")
    else:
        return render(request, 'profile.html')
