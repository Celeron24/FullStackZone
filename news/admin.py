#from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import NewsArticle

class NewsArticleAdmin(ModelAdmin):
    model = NewsArticle
    menu_label = 'News Articles'
    menu_icon = 'doc-full'  # Change as needed
    list_display = ('title', 'published_date')
    search_fields = ('title', 'description')

# Register the ModelAdmin class with Wagtail
modeladmin_register(NewsArticleAdmin)
