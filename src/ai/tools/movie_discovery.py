from langchain_core.tools import Tool
from tmdb import client as tmdb_client

def make_search_movies_tool(config):
    def _search_movies(query: str, limit: int = 5):
        user_id = config.get('configurable', {}).get('user_id')
        print('Searching movies with user', user_id)

        if limit > 25:
            limit = 25

        response = tmdb_client.search_movie(query, raw=False)

        try:
            total_results = int(response.get("total_results", -1))
        except:
            total_results = -1

        if total_results == 0:
            return []

        return response.get("results", [])[:limit]

    return Tool.from_function(
        name="search_movies",
        func=_search_movies,
        description=(
            "Search up to 25 movies from The Movie Database (TMDB) "
            "matching the query string."
        )
    )


def make_movie_detail_tool(config):
    def _movie_detail(movie_id: int):
        user_id = config.get('configurable', {}).get('user_id')
        print('Getting movie detail with user', user_id)

        response = tmdb_client.movie_detail(movie_id, raw=False)
        return response or {"error": "Movie not found."}

    return Tool.from_function(
        name="movie_detail",
        func=_movie_detail,
        description="Get detailed movie information by TMDB movie ID."
    )
