from django.urls import path
from landing_page.views import index, text_from_article, workshop_article, workshop_twitter

urlpatterns = [
    path("", index, name="home"),
    path("article-text", text_from_article, name="text_article"),
    path("workshop_article", workshop_article, name="text"),
    path("workshop_twitter", workshop_twitter, name="twitter"),
]