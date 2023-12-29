from django.shortcuts import render
from summedia.fetching_data import (
    get_text_from_article,
    article_time_read,
    get_images_from_html,
)
from summedia.text import Text
from summedia.social_media import SocialMedia
from django.conf import settings
from django.views.generic import TemplateView
from django.views import View
from .forms import URLInputForm, TextInputForm, NumericInputForm
from .base_view import BaseTextView

API_KEY = settings.OPENAI_API_KEY


class IndexView(TemplateView):
    template_name = "landing_page/home.html"


class TextView(View):
    def get(self, request):
        text_form = TextInputForm()
        numeric_form = NumericInputForm()
        return render(
            request,
            "landing_page/text.html",
            {"text_form": text_form, "numeric_form": numeric_form},
        )

    def post(self, request):
        text_form = TextInputForm(request.POST)
        numeric_form = NumericInputForm(request.POST)

        if text_form.is_valid() and numeric_form.is_valid():
            url = text_form.cleaned_data["text"]
            numeric_form = numeric_form.cleaned_data["number"]

            text = Text(api_key=API_KEY)
            summary_article = text.summarize_text(url, numeric_form)
            analyze_sentiment = text.analyze_sentiment(url)
            to_bullet_list = text.to_bullet_list(url)
            translate_text = text.translate_text(url, language_to_translate="pl")
            adjust_text_complexity = text.adjust_text_complexity(url)
            tag_and_categorize_text = text.tag_and_categorize_text(url)

            # Create a new instance of the form for rendering
            text_form = TextInputForm()
            numeric_form = NumericInputForm()

            context = {
                "summary_article": summary_article,
                "analyze_sentiment": analyze_sentiment,
                "to_bullet_list": to_bullet_list,
                "translate_text": translate_text,
                "adjust_text_complexity": adjust_text_complexity,
                "tag_and_categorize_text": tag_and_categorize_text,
                "text_form": text_form,
                "numeric_form": numeric_form,
            }
            return render(request, "landing_page/text.html", context)
        else:
            return render(
                request,
                "landing_page/text.html",
                {"text_form": text_form, "numeric_form": numeric_form},
            )


class ArticleView(View):
    def get(self, request):
        form = URLInputForm()

        return render(request, "landing_page/article.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            text_article = get_text_from_article(url)
            time_read = article_time_read(text_article)
            img_urls = get_images_from_html(url)

            text = Text(api_key=API_KEY)
            summary_article = text.summarize_text(text_article, 200)
            analyze_sentiment = text.analyze_sentiment(
                text_article, model_type="gpt-3.5-turbo-1106"
            )

            new_form = URLInputForm()

            context = {
                "text_article": text_article,
                "time_read": time_read,
                "img_urls": img_urls,
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


class SummaryTextView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/summary_text.html"
    extra_context = {"numeric_form": NumericInputForm}

    def post(self, request):
        text_form = self.form_class(request.POST)
        numeric_form = self.extra_context["numeric_form"](request.POST)

        if text_form.is_valid() and numeric_form.is_valid():
            return self.form_valid(text_form, numeric_form)
        else:
            return self.form_invalid(text_form)

    def form_valid(self, text_form, numeric_form):
        text = text_form.cleaned_data["text"]
        amount_words = numeric_form.cleaned_data["number"]
        txt = Text(api_key=API_KEY)
        summary_article = txt.summarize_text(text, amount_words)
        context = {
            "output": summary_article,
            "text_form": TextInputForm(),
            "numeric_form": NumericInputForm(),
        }

        return render(self.request, self.template_name, context)


class AnalyzeSentimentView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Analyze text sentiment"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        output = txt.analyze_sentiment(text)
        context = self.get_context_data(output=output)

        return render(self.request, self.template_name, context)


class BulletListView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Bullet list from text"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        to_bullet_list = txt.to_bullet_list(text)
        context = self.get_context_data(output=to_bullet_list)

        return render(self.request, self.template_name, context)


class TranslateTextView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Translate text"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        translate_text = txt.translate_text(text, language_to_translate="pl")
        context = self.get_context_data(output=translate_text)

        return render(self.request, self.template_name, context)


class AdjustTextComplexityView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Adjustment text complexity"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        adjust_text_complexity = txt.adjust_text_complexity(text)
        context = self.get_context_data(output=adjust_text_complexity)

        return render(self.request, self.template_name, context)


class TagAndCategorizeView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Tag and categorize text"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        tag_and_categorize_text = txt.tag_and_categorize_text(text)
        context = self.get_context_data(output=tag_and_categorize_text)

        return render(self.request, self.template_name, context)
