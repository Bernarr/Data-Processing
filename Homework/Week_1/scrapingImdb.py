#!/usr/bin/env python
# Name: Bernar van Tongeren
# Student number: 12374377
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'

def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """
    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.
    movie_containers = dom.find_all('div', class_ = 'lister-item mode-advanced')

    # list of Movie names
    # first_movie = movie_containers[0]
    # fm_name = first_movie.h3.a.text
    # year_dirty = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
    # pattern = '\d+'
    # fm_year = int(re.search(pattern, year_dirty).group(0))
    # fm_rating = float(first_movie.find('div', class_ = 'inline-block ratings-imdb-rating').strong.text)
    # fm_runtime = int(first_movie.find('p', class_ = 'text-muted ').span.text.split()[0])
    # fm_actors = first_movie.find_all('p', class_ = '')[1].text
    #
    # fm_actors = fm_actors.split('Stars:')[1].strip('\n')
    #
    # print(fm_name)
    # print(fm_year)
    # print(fm_rating)
    # print(fm_runtime)
    # print(fm_actors)

    # make list of dictionary

    pattern = '\d+'
    movies = []

    for m in movie_containers:
        movie = []
        title = m.h3.a.text
        rating = float(m.find('div', class_ = 'inline-block ratings-imdb-rating').strong.text)
        year_dirty = m.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
        year = int(re.search(pattern, year_dirty).group(0))
        actors = m.find_all('p', class_ = '')[1].text
        try:
            actors = actors.split('Stars:')[1].strip('\n')
            actors = actors.split(', \n')
            actors = ", ".join(actors)
        except:
            actors = None

        runtime = int(m.find('p', class_ = 'text-muted ').find('span', class_ = 'runtime').text.split()[0])

        movie.extend([title, rating, year, actors, runtime])
        movies.append(movie)


    return movies   # REPLACE THIS LINE AS WELL IF APPROPRIATE


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])

    for movie in movies:
        title = movie[0]
        rating = movie[1]
        year = movie[2]
        actor = movie[3]
        runtime = movie[4]
        writer.writerow([title, rating, year, actor, runtime])



def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)
    print(movies)
    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
