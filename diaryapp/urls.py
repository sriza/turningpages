from django.urls import path
from .views import landing_page, signup, login, home, logout, blog, diary, profile

urlpatterns = [
    path('', landing_page, name="landingpage"),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path("logout/", logout, name="logout"),
    path("blog/", blog, name="blog"),
    path("diary/", diary, name='diary'),
    path("profile/", profile, name="profile"),

]
