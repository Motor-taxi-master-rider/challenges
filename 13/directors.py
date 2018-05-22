# -*- coding:utf-8 -*-
import csv
import io
import operator
from collections import defaultdict, namedtuple

MOVIE_DATA = 'movie_metadata.csv'
NUM_TOP_DIRECTORS = 20
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    '''Extracts all movies from csv and stores them in a dictionary
    where keys are directors, and values is a list of movies (named tuples)'''
    director_movie = defaultdict(list)
    with open(MOVIE_DATA, encoding='utf-8') as fh:
        has_header = csv.Sniffer().has_header(fh.readline())
        fh.seek(io.SEEK_SET)
        reader = csv.DictReader(fh)
        if has_header:
            next(reader, None)
        for row in reader:
            director_movie[row['director_name']].append(Movie(title=row['movie_title'],
                                                              year=row['title_year'],
                                                              score=row['imdb_score']))
    return director_movie


def get_average_scores(directors):
    '''Filter directors with < MIN_MOVIES and calculate averge score'''
    director_info = {}
    directors_with_enough_movie = filter(
        lambda row: len(row[1]) >= MIN_MOVIES, directors.items())
    for director, movies in directors_with_enough_movie:
        director_info[director] = (_calc_mean(movies), movies)
    return director_info


def _calc_mean(movies):
    '''Helper method to calculate mean of list of Movie namedtuples'''
    return sum(float(movie.score) for movie in movies) / len(movies)


def print_results(directors):
    '''Print directors ordered by highest average rating. For each director
    print his/her movies also ordered by highest rated movie.
    See http://pybit.es/codechallenge13.html for example output'''
    def get_avg(item):
        return item[1][0]
    fmt_director_entry = '{counter}. {director:<52} {avg:.2f}'
    fmt_movie_entry = '{year}] {title:<50} {score}'
    sep_line = '-' * 60
    for counter, (director, (avg, movies)) in \
            enumerate(sorted(directors.items(), key=get_avg, reverse=True), start=1):
        print(fmt_director_entry.format(
            counter=counter, director=director, avg=avg))
        print(sep_line)
        for title, year, score in movies:
            print(fmt_movie_entry.format(year=year, title=title, score=score))
        print()


def main():
    '''This is a template, feel free to structure your code differently.
    We wrote some tests based on our solution: test_directors.py'''
    directors = get_movies_by_director()
    directors = get_average_scores(directors)
    print_results(directors)


if __name__ == '__main__':
    main()
