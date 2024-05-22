from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import PageChooserPanel
from wagtail.images.models import Image


class NewsArticle(Page):
    published_date = models.DateField()
    news_title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    image_url = models.ImageField(upload_to='images/', null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('news_title'),
        FieldPanel('description'),
        FieldPanel('link'),
        FieldPanel('image_url'),
    ]