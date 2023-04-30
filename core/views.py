from django.shortcuts import render

from movies.models import Movie
from shows.models import TvShows
from services import ScrapeMoviesService, ScrapeTvShowsService


def index(request):
    service = ScrapeMoviesService()
    top_movies = service.get_top_movies()

    for top_movie in top_movies:
        movie = (
            Movie.objects.
            filter(
                title=top_movie.get('title'),
                year=top_movie.get('year')
            )
            .first()
        )
        if movie:
            movie.poster_image = top_movie.get('poster_image')
            movie.rating = top_movie.get('rating')
            movie.save()
        else:
            movie = Movie(**top_movie)
            movie.save()

    service_shows = ScrapeTvShowsService()
    top_shows = service_shows.get_top_movies()

    for top_show in top_shows:
        show = (
            TvShows.objects.
            filter(
                poster_image=top_show.get('poster_image'),
                title=top_show.get('title'),
                year=top_show.get('year')
            )
            .first()
        )
        if show:
            show.rating = top_show.get('rating')
            show.save()
        else:
            show = TvShows(
                poster_image=top_show.get('poster_image'),
                title=top_show.get('title'),
                year=top_show.get('year'),
                rating=top_show.get('rating'),
            )
            show.save()

    return render(request, "core/index.html")


def shows(request):
    service_shows = ScrapeTvShowsService()
    top_shows = service_shows.get_top_shows()

    for top_show in top_shows:
        show = (
            TvShows.objects.
            filter(
                title=top_show.get('title'),
                year=top_show.get('year')
            )
            .first()
        )
        if show:
            show.poster_image = top_show.get('poster_image')
            show.rating = top_show.get('rating')
            show.save()
        else:
            show = TvShows(
                poster_image=top_show.get('poster_image'),
                title=top_show.get('title'),
                year=top_show.get('year'),
                rating=top_show.get('rating'),
            )
            show.save()

    return render(request, "core/index.html")
