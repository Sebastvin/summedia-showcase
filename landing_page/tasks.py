from celery import shared_task
from summedia.social_media import SocialMedia
from summedia.fetching_data import get_text

@shared_task
def post_to_facebook_task(url, api_key):
    text_article = get_text(url)
    fb = SocialMedia(api_key=api_key)
    response = fb.post_to_facebook(text_article, model_type="gpt-3.5-turbo-1106")
    return response