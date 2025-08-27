import requests
from django.conf import settings

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjOWI5YTY2Mjc0NGUxNjUyNDBiNTgwYjgwM2EyNGFmZSIsIm5iZiI6MTc1NTk2MzU5OC4yNTUsInN1YiI6IjY4YTllMGNlZWFmNWM4MmQ3ODQ0ODU5NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.LJ0W0qSAou313uU5EkvFlOjNeAQwuwlcOEGMjt7yrBA"
}

response = requests.get(url, headers=headers)

print(response.text)

def get_headers():
    return {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_API_KEY}"
}

def search_movie(query:str, page:int=1, raw= False):
    url= "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": query,
        "page": page,
        "include_adult":False,
        "language": "en-US",
    }
    headers = get_headers()
    
    response = requests.get(url, headers=headers, params=params)
    if raw:
        return response
    return response.json()

def movie_detail(movie_id:int, raw= False):
    url= f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "include_adult":False,
        "language": "en-US",
    }
    headers = get_headers()
    
    response = requests.get(url, headers=headers, params=params)
    if raw:
        return response
    return response.json()
