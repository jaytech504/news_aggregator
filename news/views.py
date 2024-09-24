from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from django.conf import settings

# Function to fetch news by category, country or search query
def get_news_data(category=None, country='us', query=None):
    api_key = settings.NEWS_API_KEY
    base_url = f'https://newsapi.org/v2/top-headlines?apiKey={api_key}'
    
    # If searching with keywords, we use the 'everything' endpoint
    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    else:
        if category:
            url = f'{base_url}&category={category}&country={country}'
        else:
            url = f'{base_url}&country={country}'
    
    response = requests.get(url)
    data = response.json()
    if data.get("status") == "ok":
        return data.get("articles", [])
    return []

def news_list(request):
    # Get category, search query, and country from request parameters
    category = request.GET.get('category', 'general')
    query = request.GET.get('search')  # Search term
    country = request.GET.get('country', 'us')  # Default country is US

    # Get the news data (based on category, search query, or country)
    if query:
        articles = get_news_data(query=query)
    else:
        articles = get_news_data(category=category, country=country)

    # Implement pagination
    paginator = Paginator(articles, 10)  # Show 5 articles per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the articles for the requested page

    return render(request, 'news/base.html', {
        'page_obj': page_obj,
        'category': category,
        'query': query,
        'country': country,
    })
