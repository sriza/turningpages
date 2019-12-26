from django.contrib import admin
from .models import UserModel, SentimentModel, SentimentcatModel

# Register your models here.

admin.site.register(UserModel)
admin.site.register(SentimentcatModel)
admin.site.register(SentimentModel)
