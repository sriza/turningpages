from django.contrib import admin
from .models import UserModel, SentimentModel, SentimentcatModel, DiaryModel

# Register your models here.

admin.site.register(UserModel)
admin.site.register(DiaryModel)
admin.site.register(SentimentcatModel)
admin.site.register(SentimentModel)
