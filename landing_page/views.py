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
    get_meta_description,
    get_meta_keywords,
)

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
from .tasks import (
    post_to_facebook_task,
    condense_text_to_tweet_task,
    summarize_text_task,
    analyze_sentiment_task,
    bullet_list_task,
    translate_text_task,
    adjust_text_complexity_task,
    tag_and_categorize_task,
)
from django.http import JsonResponse
from celery.result import AsyncResult


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
                task_id = summarize_text_task.delay(text_article, 200, API_KEY)

                time_read = get_time_read(url)
                img_urls = get_images(url)
                publish_date = get_publishing_date(url)
                authors = get_authors(url)
                title = get_title(url)
                meta_description = get_meta_description(url)
                meta_keywords = get_meta_keywords(url)

                new_form = URLInputForm()

                context = {
                    "text_article": text_article,
                    "time_read": time_read,
                    "img_urls": img_urls,
                    "publish_date": publish_date,
                    "authors": authors,
                    "title": title,
                    "meta_description": meta_description,
                    "meta_keywords": meta_keywords,
                    "task_id": task_id,
                    "form": new_form,
                }

                return render(request, "landing_page/article.html", context)
            except Exception as e:
                return render(
                    request,
                    "landing_page/article.html",
                    {
                        "form": form,
                        "error_message": True,
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
            url = form.cleaned_data["url"]

            new_form = URLInputForm()

            task_id = condense_text_to_tweet_task.delay(url, API_KEY)

            return render(
                request,
                "landing_page/twitter.html",
                {
                    "form": new_form,  # Include the form in the context
                    "task_id": task_id,
                },
            )
        else:
            # In case the form is not valid, re-render the page with the form containing validation errors
            return render(request, "landing_page/twitter.html", {"form": form})


class TaskView(View):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get("task_id")

        task_result = AsyncResult(task_id)

        return JsonResponse(
            {
                "task_id": task_id,
                "status": task_result.status,
                "result": task_result.result if task_result.ready() else None,
            }
        )


class FacebookView(View):
    def get(self, request):
        form = URLInputForm()
        return render(request, "landing_page/facebook.html", {"form": form})

    def post(self, request):
        form = URLInputForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data["url"]

                task_id = post_to_facebook_task.delay(url, API_KEY)

                return render(
                    request,
                    "landing_page/facebook.html",
                    {"form": URLInputForm, "task_id": task_id},
                )
            except Exception as e:
                print(f"Error in submitting task: {e}")
                return render(
                    request,
                    "landing_page/facebook.html",
                    {
                        "form": form,
                        "error_message": "Download error",
                        "error_helper": "Ensure the URL is correct and accessible.",
                    },
                )
        else:
            return render(request, "landing_page/facebook.html", {"form": form})


class SocialMediaView(View):
    @staticmethod
    def get(request):
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

        task_id = summarize_text_task.delay(text, amount_words, API_KEY)

        context = {
            "text_form": text_form,
            "numeric_form": NumericInputForm(),
            "title": self.title,
            "task_id": task_id,
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

        task_id = analyze_sentiment_task.delay(text, amount_words, API_KEY)

        context = {
            "task_id": task_id,
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
        task_id = bullet_list_task.delay(text, API_KEY)

        context = {
            "task_id": task_id,
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

        task_id = translate_text_task.delay(text, language, API_KEY)

        context = {
            "task_id": task_id,
            "text_form": text_form,
            "language_form": language_form,
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

        task_id = adjust_text_complexity_task.delay(text, complexity, API_KEY)

        context = {
            "task_id": task_id,
            "text_form": text_form,
            "complexity_form": complexity_form,
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

        task_id = tag_and_categorize_task.delay(text, API_KEY)

        context = {
            "task_id": task_id,
            "text_form": text_form,
            "title": self.title,
        }

        return render(self.request, self.template_name, context)
