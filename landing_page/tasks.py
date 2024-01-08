from celery import shared_task
from summedia.social_media import SocialMedia
from summedia.fetching_data import get_text
from summedia.text import Text
from summedia.level import SimplificationLevel


@shared_task
def post_to_facebook_task(url, api_key):
    response = {"success": False, "error": None, "data": None}

    try:
        text_article = get_text(url)
        fb = SocialMedia(api_key=api_key)
        response = fb.post_to_facebook(text_article, model_type="gpt-3.5-turbo-1106")

        print(response)

        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def condense_text_to_tweet_task(url, api_key):
    try:
        text_article = get_text(url)
        twitter = SocialMedia(api_key=api_key)
        response = twitter.condense_text_to_tweet(
            text_article, model_type="gpt-3.5-turbo-1106"
        )
        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def summarize_text_task(text, amount_words, api_key):
    try:
        txt = Text(api_key=api_key)
        response = txt.summarize_text(text, amount_words)
        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def analyze_sentiment_task(text, amount_words, api_key):
    try:
        txt = Text(api_key=api_key)
        response = txt.analyze_sentiment(text, amount_words)
        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def bullet_list_task(text, api_key):
    try:
        txt = Text(api_key=api_key)
        response = txt.to_bullet_list(text)
        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def translate_text_task(text, language, api_key):
    try:
        txt = Text(api_key=api_key)
        response = txt.translate_text(text, language_to_translate=language)
        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def adjust_text_complexity_task(text, complexity, api_key):
    try:
        txt = Text(api_key=api_key)
        level = SimplificationLevel[complexity]
        response = txt.adjust_text_complexity(text, level=level)
        return response
    except Exception as e:
        print(e)
        return "ERROR"


@shared_task
def tag_and_categorize_task(text, api_key):
    try:
        txt = Text(api_key=api_key)
        response = txt.tag_and_categorize_text(text)
        return response
    except Exception as e:
        print(e)
        return "ERROR"
