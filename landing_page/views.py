from django.shortcuts import render
from summedia.fetching_data import (
    get_text_from_article,
    article_time_read,
    get_images_from_html,
)
from summedia.text import Text
from summedia.social_media import SocialMedia
from django.conf import settings
import openai
from django.views.generic import TemplateView
from django.views import View
from .forms import URLInputForm, TextInputForm

API_KEY = settings.OPENAI_API_KEY


# Create your views here.
class IndexView(TemplateView):
    template_name = "landing_page/home.html"


class TextView(View):
    def get(self, request):
        form = TextInputForm()
        return render(request, "landing_page/text.html", {"form": form})

    def post(self, request):
        form = TextInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["text"]

            text = Text(api_key=API_KEY)
            summary_article = text.summarize_text(url, 200)
            analyze_sentiment = text.analyze_sentiment(url)
            to_bullet_list = text.to_bullet_list(url)
            translate_text = text.translate_text(url, language_to_translate="pl")
            adjust_text_complexity = text.adjust_text_complexity(url)
            tag_and_categorize_text = text.tag_and_categorize_text(url)

            # Create a new instance of the form for rendering
            new_form = TextInputForm()

            context = {
                "summary_article": summary_article,
                "analyze_sentiment": analyze_sentiment,
                "to_bullet_list": to_bullet_list,
                "translate_text": translate_text,
                "adjust_text_complexity": adjust_text_complexity,
                "tag_and_categorize_text": tag_and_categorize_text,
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
                text_article, model_type="gpt-3.5-turbo-1106"
            )

            new_form = URLInputForm()

            context = {
                "analyze_sentiment": analyze_sentiment,
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
            twitter = SocialMedia(api_key=API_KEY)
            condense_text_to_tweet = twitter.condense_text_to_tweet(
                text_article, model_type="gpt-3.5-turbo-1106"
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


class FacebookView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/facebook.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            fb = SocialMedia(api_key=API_KEY)
            post_to_facebook = fb.post_to_facebook(
                text_article, model_type="gpt-3.5-turbo-1106"
            )

            new_form = URLInputForm()

            context = {
                "form": new_form,  # Include the form in the context
                "post_to_facebook": post_to_facebook,
            }
            return render(request, "landing_page/facebook.html", context)
        else:
            # In case the form is not valid, re-render the page with the form containing validation errors
            return render(request, "landing_page/facebook.html", {"form": form})


class SocialMediaView(View):
    def get(self, request):
        return render(request, "landing_page/social_media.html")
