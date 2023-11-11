from django.urls import path
from landing_page.views import (
    IndexView,
    TextView,
    WorkshopArticleView,
    WorkshopTwitterView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("text", TextView.as_view(), name="text"),
    path("article", WorkshopArticleView.as_view(), name="article"),
    path("twitter", WorkshopTwitterView.as_view(), name="twitter"),
]
