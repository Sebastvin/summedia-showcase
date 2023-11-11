from django.urls import path
from landing_page.views import IndexView, TextView, ArticleView, TwitterView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("text", TextView.as_view(), name="text"),
    path("article", ArticleView.as_view(), name="article"),
    path("twitter", TwitterView.as_view(), name="twitter"),
]