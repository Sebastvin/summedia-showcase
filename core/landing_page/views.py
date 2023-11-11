from django.shortcuts import render
from engineer_demo.fetching_data import (
    get_text_from_article,
    article_time_read,
    get_images_from_html,
)
from engineer_demo.text import Text
from engineer_demo.twitter import Twitter
from django.conf import settings
import openai
from django.views.generic import TemplateView
from django.views import View
from .forms import URLInputForm

openai.api_key = settings.OPENAI_API_KEY


# Create your views here.
class IndexView(TemplateView):
    template_name = "landing_page/home.html"


class TextView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/input_form.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)

            time_read = article_time_read(text_article)

            img_urls = get_images_from_html(url)

            return render(
                request,
                "landing_page/text.html",
                {"text": text_article, "time_read": time_read, "img_urls": img_urls},
            )
        return render(request, "landing_page/input_form.html", {"form": form})


class WorkshopArticleView(View):
    def get(self, request):
        form = URLInputForm()

        return render(request, "landing_page/input_form.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            text = Text()
            analyze_sentiment = text.analyze_sentiment(text_article)
            return render(
                request,
                "landing_page/article.html",
                {"analyze_sentiment": analyze_sentiment, "text_article": text_article},
            )


class WorkshopTwitterView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/input_form.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            twitter = Twitter()
            condense_text_to_tweet = twitter.condense_text_to_tweet(text_article)
            return render(
                request,
                "landing_page/twitter.html",
                {"condense_text_to_tweet": condense_text_to_tweet},
            )
