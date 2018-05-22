from directors import _calc_mean, get_average_scores, get_movies_by_director


def test():
    directors = get_movies_by_director()

    assert 'Sergio Leone' in directors
    assert 'Andrew Stanton' in directors  # has 3 movies, but not yet filtered
    assert len(directors['Sergio Leone']) == 4
    assert len(directors['Peter Jackson']) == 12

    movies_sergio = directors['Sergio Leone']
    movies_nolan = directors['Christopher Nolan']
    assert round(_calc_mean(movies_sergio), 1) == 8.5
    assert round(_calc_mean(movies_nolan), 1) == 8.4

    directors = get_average_scores(directors)
    assert 'Andrew Stanton' not in directors  #  director 3 movies now filtered out

    expected_directors = ['Sergio Leone', 'Christopher Nolan', 'Hayao Miyazaki',
                          'Quentin Tarantino',  'Frank Capra','Stanley Kubrick']
    expected_avg_scores = [8.5, 8.4, 8.2, 8.2, 8.1, 8.0]
    expected_num_movies = [4, 8, 4, 8, 5, 7]
    report = sorted(directors.items(),
                    key=lambda x: float(x[1][0]), reverse=True)
    for counter, (i, j, k) in enumerate(
        zip(expected_directors,
            expected_avg_scores, expected_num_movies)):
        assert report[counter][0] == i
        assert len(report[counter][1][1]) == k
        assert round(_calc_mean(report[counter][1][1]), 1) == j

    return "tests pass"


if __name__ == '__main__':
    print(test())
