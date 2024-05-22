from django.core.management.base import BaseCommand
from django.utils.text import slugify
import feedparser
from dateutil import parser as date_parser
from news.models import NewsArticle, Page  # Adjust import according to your app structure
from news.utils import save_image_from_url  # Adjust import according to your utility function


class Command(BaseCommand):
    help = 'Import RSS feed entries into the NewsArticle model'

    def handle(self, *args, **kwargs):
        rss_urls = [
            "https://feeds.bbci.co.uk/news/rss.xml",
            # "https://rss.cnn.com/rss/edition.rss",
            # "https://www.yahoo.com/news/rss",
            # "https://www.thenews.com.pk/rss/1/1",
            # "https://www.thenews.com.pk/rss/1/8",
            # "https://www.thenews.com.pk/rss/2/14",
            # "https://feeds.bbci.co.uk/news/rss.xml",
            # "https://feeds.bbci.co.uk/news/world/rss.xml",
            # "https://feeds.bbci.co.uk/news/business/rss.xml",
            # "https://feeds.bbci.co.uk/news/health/rss.xml",
            # Add more RSS feed URLs here
        ]

        home_page = Page.objects.get(slug='home')  # Ensure you have a home page

        for rss_url in rss_urls:
            feed = feedparser.parse(rss_url)
            entries = feed.entries

            for entry in entries:
                title = entry.get('title')
                link = entry.get('link')[:200]  # Truncate link if it exceeds 200 characters
                summary = entry.get('summary', 'No description available.')

                published_date_str = entry.get('published')
                published_date = date_parser.parse(published_date_str) if published_date_str else None

                image_url = None
                if 'media_thumbnail' in entry and entry['media_thumbnail']:
                    image_url = entry['media_thumbnail'][0]['url']

                # Check if the news article already exists
                news_article = NewsArticle.objects.child_of(home_page).filter(news_title=title).first()

                if news_article:
                    # Update existing article
                    news_article.link = link
                    news_article.description = summary
                    news_article.published_date = published_date

                    if image_url:
                        image_content = save_image_from_url(image_url, title, f"{slugify(title)}.jpg")
                        if image_content:
                            news_article.image_url.save(
                                f"{slugify(title)}.jpg",
                                image_content,
                                save=False
                            )

                    news_article.save()
                else:
                    # Create new article
                    news_article = NewsArticle(
                        title=title,
                        slug=slugify(title),
                        news_title=title,
                        link=link,
                        description=summary,
                        published_date=published_date,
                    )

                    if image_url:
                        image_content = save_image_from_url(image_url, title, f"{slugify(title)}.jpg")
                        if image_content:
                            news_article.image_url.save(
                                f"{slugify(title)}.jpg",
                                image_content,
                                save=False
                            )

                    home_page.add_child(instance=news_article)
                    news_article.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported RSS feed entries'))
