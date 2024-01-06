from celery import shared_task
from summedia.social_media import SocialMedia
from summedia.fetching_data import get_text


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
