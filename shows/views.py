from django.shortcuts import render

from shows.models import TvShows


# Create your views here.
def top_shows(request):
    shows = TvShows.objects.all()

    context = {
        'shows': shows
    }
    return render(request, template_name='core/shows.html', context=context)
