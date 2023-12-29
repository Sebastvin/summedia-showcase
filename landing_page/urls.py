from django.urls import path
from landing_page.views import (
    IndexView,
    TextView,
    ArticleView,
    TwitterView,
    FacebookView,
    SocialMediaView,
    SummaryTextView,
    AnalyzeSentimentView,
    BulletListView,
    TranslateTextView,
    AdjustTextComplexityView,
    TagAndCategorizeView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("article", ArticleView.as_view(), name="article"),
    path("twitter", TwitterView.as_view(), name="twitter"),
    path("facebook", FacebookView.as_view(), name="facebook"),
    path("social", SocialMediaView.as_view(), name="social"),
    path("text", TextView.as_view(), name="text"),
    path("text/summary-text", SummaryTextView.as_view(), name="summary_text"),
    path(
        "text/analyze-sentiment",
        AnalyzeSentimentView.as_view(),
        name="analyze_sentiment",
    ),
    path("text/bullet-list", BulletListView.as_view(), name="bullet_list"),
    path("text/translate-text", TranslateTextView.as_view(), name="translate_text"),
    path(
        "text/adjust-text-complexity",
        AdjustTextComplexityView.as_view(),
        name="adjust_text_complexity",
    ),
    path(
        "text/tag-and-categorize",
        TagAndCategorizeView.as_view(),
        name="tag_and_categorize",
    ),
]
