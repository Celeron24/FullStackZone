from datetime import datetime, time
import requests
from news.models import NewsArticle
from django.shortcuts import render
from dateutil import parser as date_parser
from django.shortcuts import render
from .forms import RSSFeedSearchForm, ArchiveNewsSearchForm
from .models import NewsArticle
from wagtail.models import Page
from wagtail.images.models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import feedparser
from django.utils.dateparse import parse_date


def save_image_from_url(url, title):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content, name=f"{slugify(title)}.jpg")
    return None

def health():
    bbc_rss_url = "https://feeds.bbci.co.uk/news/health/rss.xml"
    feed = feedparser.parse(bbc_rss_url)

    bbc_news = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary

        bbc_news.append({
            'title': title,
            'link': link,
            'summary': summary
        })

    return bbc_news

def Sports(request):
    bbc_sports_news_articles = NewsArticle.objects.filter(news_title__icontains='business')
    return render(request, 'newshub/Sports.html', {'bbc_sports_news_articles': bbc_sports_news_articles})


def index(request):
    form = RSSFeedSearchForm(request.POST or None)
    rss_url = "https://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(rss_url)
    entries = []

    for entry in feed.entries:
        title = entry.get('title')
        link = entry.get('link')
        summary = entry.get('summary')
        image_url = None

        # Check if there is a media thumbnail available
        if 'media_thumbnail' in entry and entry['media_thumbnail']:
            image_url = entry['media_thumbnail'][0]['url']

        entries.append({
            'title': title,
            'link': link,
            'summary': summary,
            'image_url': image_url
        })

    return render(request, 'newshub/index.html', {'entries': entries, 'form': form})


def archive(request):
    form = ArchiveNewsSearchForm(request.POST or None)
    archived_news = None
    news = NewsArticle.objects.all()
    if request.method == 'POST':
        form = ArchiveNewsSearchForm(request.POST)
        if form.is_valid():
            filter_archive_date = form.cleaned_data['filter_archive_date']
            archived_news = NewsArticle.objects.filter(published_date__date=filter_archive_date)

    return render(request, 'newshub/archived_news.html', {'form': form, 'archived_news': archived_news, 'news': news})



def parse_date(date_str):
    try:
        parsed_date = date_parser.parse(date_str)
        return parsed_date.date()
    except ValueError:
        return None

def extract_image_url(entry):
    # Check if 'summary' field exists and extract image URL from it
    if 'summary' in entry:
        summary = entry['summary']
        # Extracting image URL from the summary
        start_index = summary.find('<img src="') + len('<img src="')
        end_index = summary.find('"', start_index)
        image_url = summary[start_index:end_index]
        return image_url
    return None

def search_feed(feed, query, start_date, end_date):
    results = []
    for entry in feed.entries:
        published_date = parse_date(entry.published)
        if published_date and start_date <= published_date <= end_date:
            if query.lower() in entry.title.lower() or (entry.summary and query.lower() in entry.summary.lower()):
                # Extract image URL
                image_url = extract_image_url(entry)
                entry['image_url'] = image_url  # Add image URL to the entry dictionary
                results.append(entry)
    return results

def rss_feed_search(request):
    form = RSSFeedSearchForm(request.POST or None)
    search_results = []

    if request.method == 'POST' and form.is_valid():
        query = form.cleaned_data['query']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        rss_urls = [
            "https://feeds.bbci.co.uk/news/rss.xml?edition=int",
            # "https://www.yahoo.com/news/rss",
            # "https://www.thenews.com.pk/rss/1/1",
            # "https://www.thenews.com.pk/rss/1/8",
            # "https://www.thenews.com.pk/rss/2/14",
        ]

        for rss_url in rss_urls:
            try:
                feed = feedparser.parse(rss_url)
                if feed.status == 200:
                    search_results.extend(search_feed(feed, query, start_date, end_date))
            except Exception:
                pass

    context = {
        'form': form,
        'search_results': search_results,
    }
    return render(request, 'newshub/search.html', context)
