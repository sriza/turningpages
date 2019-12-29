from django.db import models

# Create your models here.


class UserModel(models.Model):
    name = models.CharField(max_length=120)
    gender = models.CharField(max_length=10, default="none")
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=25)


class DiaryModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    polarity = models.IntegerField()


class SentimentcatModel(models.Model):
    sentiment = models.CharField(max_length=50)
    sentiment_img = models.ImageField(upload_to="SentimentImg")


class UserprofileModel(models.Model):
    user_img = models.ImageField(upload_to="media")


class SentimentModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sentiment = models.ForeignKey(SentimentcatModel, on_delete=models.CASCADE)
