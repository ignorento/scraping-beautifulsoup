from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

import config_base


class ScrapeMoviesService:

    url = "https://www.imdb.com/chart/top"
    count_tags = 250

    def get_top_movies(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        poster_tags = soup.find_all('td', class_="posterColumn")
        title_tags = soup.find_all('td', class_="titleColumn")
        rating_tags = soup.find_all('td', class_="ratingColumn imdbRating")

        assert len(poster_tags) == len(title_tags) == len(rating_tags) == self.count_tags, "Error occurred while scraping "  # noqa

        results = []
        for i in range(len(poster_tags)):
            poster_image = self.parse_poster_image(tag=poster_tags[i])
            title = self.parse_title(tag=title_tags[i])
            year = self.parse_year(tag=title_tags[i])
            rating = self.parse_rating(tag=rating_tags[i])

            results.append(
                {
                    'poster_image': poster_image,
                    'title': title,
                    'year': year,
                    'rating': rating
                }
            )
        return results

    def parse_poster_image(self, tag):
        return tag.find('img')['src']

    def parse_title(self, tag):
        return tag.find('a').text

    def parse_year(self, tag):
        return int(tag.find('span').text[1:-1])

    def parse_rating(self, tag):
        try:
            float(tag.find('strong').text)
        except AttributeError:
            return 0.0
        return float(tag.find('strong').text)


class ScrapeTvShowsService(ScrapeMoviesService):

    url = "https://www.imdb.com/chart/tvmeter"
    count_tags = 100


if __name__ == "__main__":
    service_movies = ScrapeMoviesService()
    service_shows = ScrapeTvShowsService()
    top_movies = service_movies.get_top_movies()
    top_shows = service_shows.get_top_movies()

    df_movies = pd.DataFrame.from_dict(top_movies)
    output_file_path_movies = Path(config_base.basedir) / 'movies.csv'
    df_movies.to_csv(Path(output_file_path_movies))

    df_shows = pd.DataFrame.from_dict(top_shows)
    output_file_path_shows = Path(config_base.basedir) / 'shows.csv'
    df_shows.to_csv(Path(output_file_path_shows))
