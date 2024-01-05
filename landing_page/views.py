from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from summedia.fetching_data import (
    get_text,
    get_time_read,
    get_images,
    get_publishing_date,
    get_authors,
    get_title,
    get_movies,
    get_meta_description,
    get_meta_keywords,
)
from summedia.social_media import SocialMedia
from summedia.text import Text

from .base_view import BaseTextView
from .forms import (
    NumericInputForm,
    TextInputForm,
    URLInputForm,
    LanguageForm,
    TextComplexityForm,
)
from summedia.level import SimplificationLevel


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


class ArticleView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/article.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            try:
                text_article = get_text(url)
                time_read = get_time_read(url)
                img_urls = get_images(url)
                publish_date = get_publishing_date(url)
                authors = get_authors(url)
                title = get_title(url)
                movies = get_movies(url)
                meta_description = get_meta_description(url)
                meta_keywords = get_meta_keywords(url)

                text = Text(api_key=API_KEY)
                summary_article = text.summarize_text(text_article, 200)

                new_form = URLInputForm()

                context = {
                    "text_article": text_article,
                    "time_read": time_read,
                    "img_urls": img_urls,
                    "publish_date": publish_date,
                    "authors": authors,
                    "title": title,
                    "movies": movies,
                    "meta_description": meta_description,
                    "meta_keywords": meta_keywords,
                    "summary_article": summary_article,
                    "form": new_form,
                }

                return render(request, "landing_page/article.html", context)
            except Exception as e:
                return render(
                    request,
                    "landing_page/article.html",
                    {
                        "form": form,
                        "error_message": "Download error",
                        "error_helper": "Make sure the URL is correct, no captcha security or the URL is for article",
                    },
                )

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
            try:
                url = form.cleaned_data["url"]
                text_article = get_text(url)
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
            except Exception as e:
                return render(
                    request,
                    "landing_page/twitter.html",
                    {
                        "form": form,
                        "error_message": "Download error",
                        "error_helper": "Make sure the URL is correct, no captcha security or the URL is for article",
                    },
                )
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
            try:
                url = form.cleaned_data["url"]
                text_article = get_text(url)
                social = SocialMedia(api_key=API_KEY)

                post_to_facebook = social.post_to_facebook(
                    text_article, model_type="gpt-3.5-turbo-1106"
                )

                # Stress test
                a_ = social.condense_text_to_tweet(
                    text_article, model_type="gpt-3.5-turbo-1106"
                )
                b_ = social.condense_text_to_tweet(
                    text_article, model_type="gpt-3.5-turbo-1106"
                )

                new_form = URLInputForm()

                context = {
                    "form": new_form,  # Include the form in the context
                    "post_to_facebook": post_to_facebook,
                }
                return render(request, "landing_page/facebook.html", context)
            except Exception as e:
                return render(
                    request,
                    "landing_page/facebook.html",
                    {
                        "form": form,
                        "error_message": "Download error",
                        "error_helper": "Make sure the URL is correct, no captcha security or the URL is for article",
                    },
                )
        else:
            # In case the form is not valid, re-render the page with the form containing validation errors
            return render(request, "landing_page/facebook.html", {"form": form})


class SocialMediaView(View):
    def get(self, request):
        return render(request, "landing_page/social_media.html")


class SummaryTextView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    extra_context = {"numeric_form": NumericInputForm}
    title = "Summary Text"

    def post(self, request):
        text_form = self.form_class(request.POST)
        numeric_form = self.extra_context["numeric_form"](request.POST)

        if text_form.is_valid() and numeric_form.is_valid():
            return self.form_valid(text_form, numeric_form)
        else:
            return self.form_invalid()

    def form_valid(self, text_form, numeric_form):
        text = text_form.cleaned_data["text"]
        amount_words = numeric_form.cleaned_data["number"]
        txt = Text(api_key=API_KEY)
        summary_article = txt.summarize_text(text, amount_words)
        context = {
            "output": summary_article,
            "text_form": text_form,
            "numeric_form": NumericInputForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)

    def form_invalid(self):
        context = {
            "text_form": TextInputForm(),
            "numeric_form": NumericInputForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)


class AnalyzeSentimentView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    extra_context = {"numeric_form": NumericInputForm}
    title = "Analyze text sentiment"

    def post(self, request):
        text_form = self.form_class(request.POST)
        numeric_form = self.extra_context["numeric_form"](request.POST)

        if text_form.is_valid() and numeric_form.is_valid():
            return self.form_valid(text_form, numeric_form)
        else:
            return self.form_invalid()

    def form_valid(self, text_form, numeric_form):
        text = text_form.cleaned_data["text"]
        amount_words = numeric_form.cleaned_data["number"]

        txt = Text(api_key=API_KEY)
        analyze_sentiment = txt.analyze_sentiment(text, amount_words)

        context = {
            "output": analyze_sentiment,
            "text_form": text_form,
            "numeric_form": NumericInputForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)

    def form_invalid(self):
        context = {
            "text_form": text_form,
            "numeric_form": NumericInputForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)


class BulletListView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Bullet list from text"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        to_bullet_list = txt.to_bullet_list(text)

        context = {
            "output": to_bullet_list,
            "text_form": text_form,
            "title": self.title,
        }

        return render(self.request, self.template_name, context)


class TranslateTextView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    extra_context = {"language_form": LanguageForm}
    title = "Translate text"

    def post(self, request):
        text_form = self.form_class(request.POST)
        language_form = self.extra_context["language_form"](request.POST)

        if text_form.is_valid() and language_form.is_valid():
            return self.form_valid(text_form, language_form)
        else:
            return self.form_invalid()

    def form_valid(self, text_form, language_form):
        text = text_form.cleaned_data["text"]
        language = language_form.cleaned_data["language"]

        txt = Text(api_key=API_KEY)
        translate_text = txt.translate_text(text, language_to_translate=language)

        context = {
            "output": translate_text,
            "text_form": text_form,
            "language_form": LanguageForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)


class AdjustTextComplexityView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    extra_context = {"complexity_form": TextComplexityForm}
    title = "Adjustment text complexity"

    def post(self, request):
        text_form = self.form_class(request.POST)
        complexity_form = self.extra_context["complexity_form"](request.POST)

        if text_form.is_valid() and complexity_form.is_valid():
            return self.form_valid(text_form, complexity_form)
        else:
            return self.form_invalid()

    def form_valid(self, text_form, complexity_form):
        text = text_form.cleaned_data["text"]
        complexity = complexity_form.cleaned_data["complexity"]
        txt = Text(api_key=API_KEY)

        level = SimplificationLevel[complexity]

        adjust_text_complexity = txt.adjust_text_complexity(text, level=level)

        context = {
            "output": adjust_text_complexity,
            "text_form": text_form,
            "complexity_form": TextComplexityForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)

    def form_invalid(self):
        context = {
            "text_form": TextInputForm(),
            "complexity_form": TextComplexityForm(),
            "title": self.title,
        }

        return render(self.request, self.template_name, context)


class TagAndCategorizeView(BaseTextView):
    form_class = TextInputForm
    template_name = "landing_page/text_output.html"
    title = "Tag and categorize text"

    def form_valid(self, text_form):
        text = text_form.cleaned_data["text"]
        txt = Text(api_key=API_KEY)
        tag_and_categorize_text = txt.tag_and_categorize_text(text)

        context = {
            "output": tag_and_categorize_text,
            "text_form": text_form,
            "title": self.title,
        }

        return render(self.request, self.template_name, context)
