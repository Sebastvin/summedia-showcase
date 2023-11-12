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

API_KEY = settings.OPENAI_API_KEY


# Create your views here.
class IndexView(TemplateView):
    template_name = "landing_page/home.html"


class TextView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/text.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            time_read = article_time_read(text_article)
            img_urls = get_images_from_html(url)

            # Create a new instance of the form for rendering
            new_form = URLInputForm()

            context = {
                "text": text_article,
                "time_read": time_read,
                "img_urls": img_urls,
                "form": new_form,
            }

            return render(request, "landing_page/text.html", context)
        else:
            return render(request, "landing_page/text.html", {"form": form})


class ArticleView(View):
    def get(self, request):
        form = URLInputForm()

        return render(request, "landing_page/article.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            text = Text(api_key=API_KEY)
            summary_article = text.summarize_text(text_article, 200)
            analyze_sentiment = text.analyze_sentiment(
                text_article, model_type="gpt-4-1106-preview"
            )

            new_form = URLInputForm()

            context = {
                "analyze_sentiment": analyze_sentiment,
                "text_article": text_article,
                "summary_article": summary_article,
                "form": new_form,
            }

            return render(request, "landing_page/article.html", context)
        else:
            # In case the form is not valid, re-render the page with the form containing validation errors
            return render(request, "landing_page/article.html", {"form": form})


class TwitterView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/twitter.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            twitter = Twitter(api_key=API_KEY)
            condense_text_to_tweet = twitter.condense_text_to_tweet(
                text_article, model_type="gpt-4-1106-preview"
            )

            new_form = URLInputForm()

            context = {
                "form": new_form,  # Include the form in the context
                "condense_text_to_tweet": condense_text_to_tweet,
            }
            return render(request, "landing_page/twitter.html", context)
        else:
            # In case the form is not valid, re-render the page with the form containing validation errors
            return render(request, "landing_page/twitter.html", {"form": form})
