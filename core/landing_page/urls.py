from django.urls import path
from landing_page.views import IndexView, TextView, WorkshopArticleView, WorkshopTwitterView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("article-text", TextView.as_view(), name="text_article"),
    path("workshop_article", WorkshopArticleView.as_view(), name="text"),
    path("workshop_twitter", WorkshopTwitterView.as_view(), name="twitter"),
]