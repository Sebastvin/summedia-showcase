from django.shortcuts import render
from engineer_demo.fetching_data import get_text_from_article
from engineer_demo.text import Text
from engineer_demo.twitter import Twitter
from django.views.decorators.cache import cache_page
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

# Create your views here.
def index(request):
    return render(request, "landing_page/home.html",)

@cache_page(60 * 15)
def get_text_article(request):
    text_article = text_from_article(request)
    return render(request, "landing_page/article_text.html", {"text": text_article})

def text_from_article(request):
    text_article = get_text_from_article("https://www.indiehackers.com/post/from-0-to-10-billion-the-story-of-notion-bffad92145")
    return render(request, "landing_page/article_text.html", {"text": text_article})

def workshop_article(request):
    text = Text()

    text_article = get_text_article(request)

    analyze_sentiment = text.analyze_sentiment(text_article)

    return render(request, "landing_page/text.html", {"analyze_sentiment": analyze_sentiment, "text_article": text_article})


def workshop_twitter(request):
    twitter = Twitter()

    text_article = get_text_article(request)
    condense_text_to_tweet = twitter.condense_text_to_tweet(text_article)

    return render(request, "landing_page/twitter.html", {"condense_text_to_tweet": condense_text_to_tweet})

