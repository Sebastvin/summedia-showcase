from celery import shared_task
from summedia.social_media import SocialMedia
from summedia.fetching_data import get_text
import time


@shared_task
def post_to_facebook_task(url, api_key):
    try:
        text_article = get_text(url)
        fb = SocialMedia(api_key=api_key)
        response = fb.post_to_facebook(text_article, model_type="gpt-3.5-turbo-1106")

        time.sleep(33)

        return response
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in posting to Facebook: {e}")
        return {"error": str(e)}  # Return error information


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
        # Log the exception for debugging
        print(f"Error in posting to Facebook: {e}")
        return {"error": str(e)}  # Return error information
