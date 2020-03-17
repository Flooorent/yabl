import numpy as np
import pandas as pd
import pytest

from yabl.functions import (
    get_all_categories,
    get_pct_books_read,
    get_random_unread_book,
    get_repartition_per_category,
)


class TestGetPctBooksRead:
    def test_get_pct_books_read(self):
        df = pd.DataFrame(data={'read': [1, 1, 1, 0, 0]})
        expected = 0.6
        actual = get_pct_books_read(df)
        assert actual == expected

    def test_zero_read(self):
        df = pd.DataFrame(data={'read': [0, 0, 0]})
        expected = 0.0
        actual = get_pct_books_read(df)
        assert actual == expected

    def test_zero_un_read(self):
        df = pd.DataFrame(data={'read': [1, 1, 1]})
        expected = 1.0
        actual = get_pct_books_read(df)
        assert actual == expected

    def test_should_raise_error_on_empty_df(self):
        df = pd.DataFrame(columns=['read'])

        with pytest.raises(ValueError):
            get_pct_books_read(df)


class TestGetRepartitionPerCategory:
    def test_get_repartition_per_category(self):
        df = pd.DataFrame(data={
            'read': [1, 1, 1, 0, 1, 0, 0],
            'tags': ['roman', 'roman, classique', 'roman', 'roman', 'psycho', 'classique', 'bd'],
        })

        expected_repartitions = {
            'roman': {
                'count': 4,
                'pct': 0.75,
            },
            'classique': {
                'count': 2,
                'pct': 0.5,
            },
            'psycho': {
                'count': 1,
                'pct': 1.0,
            },
            'bd': {
                'count': 1,
                'pct': 0.0,
            },
        }

        actual_repartitions = get_repartition_per_category(df)
        assert actual_repartitions == expected_repartitions

    def test_should_raise_error_on_empty_df(self):
        df = pd.DataFrame(columns=['read'])

        with pytest.raises(ValueError):
            get_repartition_per_category(df)


class TestGetRandomUnreadBook:
    def test_return_none_if_no_unread_book(self):
        df = pd.DataFrame(data={
            'read': [1, 1],
            'title': ['title1', 'title2'],
            'author': ['author1', 'author2'],
            'tags': ['novel', 'bio, history']
        })

        actual = get_random_unread_book(df)
        assert actual is None

    def test_return_one_book_at_random(self):
        unread_titles = ['title1', 'title2']
        read_titles = ['title3', 'title4']

        unread_authors = ['author1', 'author2']
        read_authors = ['author3', 'author4']

        unread_tags = ['bio', 'history, classic']
        read_tags = ['novel', 'sci-fi']

        df = pd.DataFrame(data={
            'read': [1, 1, 0, 0],
            'title': read_titles + unread_titles,
            'author': read_authors + unread_authors,
            'tags': read_tags + unread_tags,
        })

        random_book = get_random_unread_book(df)
        assert random_book.title in unread_titles
        assert random_book.author in unread_authors
        assert random_book.tags in unread_tags

    def test_replace_nan_by_empty_string(self):
        df = pd.DataFrame(data={
            'read': [1, 1, 0],
            'title': ['title1', 'title2', 'title3'],
            'author': ['author1', 'author2', np.nan],
            'tags': ['novel', 'sci-fi', np.nan],
        })

        random_book = get_random_unread_book(df)
        assert random_book.title == 'title3'
        assert random_book.author == ''
        assert random_book.tags == ''

    def test_return_none_if_no_unread_book_with_category(self):
        df = pd.DataFrame(data={
            'read': [0, 0, 1],
            'title': ['title1', 'title2', 'title3'],
            'author': ['author1', 'author2', 'author3'],
            'tags': ['novel', 'bio, history', 'sci-fi'],
        })

        actual = get_random_unread_book(df, 'sci-fi')
        assert actual is None

    def test_return_one_book_at_random_with_category(self):
        df = pd.DataFrame(data={
            'read': [0, 0, 0],
            'title': ['title1', 'title2', 'title3'],
            'author': ['author1', 'author2', 'author3'],
            'tags': ['novel', 'bio', 'bio'],
        })

        actual = get_random_unread_book(df, 'bio')
        assert actual.title in ['title2', 'title3']
        assert actual.author in ['author2', 'author3']
        assert actual.tags == 'bio'

    def test_return_one_book_at_random_with_category_among_multiple_categories(self):
        df = pd.DataFrame(data={
            'read': [0, 0],
            'title': ['title1', 'title2'],
            'author': ['author1', 'author2'],
            'tags': ['novel', 'history, bio'],
        })

        actual = get_random_unread_book(df, 'bio')
        assert actual.title == 'title2'
        assert actual.author == 'author2'
        assert actual.tags == 'history, bio'


class TestGetAllCategories:
    def test_return_empty_list_if_no_books(self):
        df = pd.DataFrame(columns=['read', 'author', 'tags'])
        actual_categories = get_all_categories(df)
        assert actual_categories == []

    def test_return_empty_list_if_no_categories(self):
        df = pd.DataFrame(data={
            'read': [1, 0],
            'author': ['author1', 'author2'],
            'tags': ['', np.nan],
        })

        actual_categories = get_all_categories(df)
        assert actual_categories == []

    def test_return_list_of_categories(self):
        df = pd.DataFrame(data={
            'read': [1, 0],
            'author': ['author1', 'author2'],
            'tags': ['sci-fi', 'novel'],
        })

        actual_categories = get_all_categories(df)
        assert isinstance(actual_categories, list)
        assert sorted(actual_categories) == sorted(['sci-fi', 'novel'])

    def test_return_list_of_deduplicated_categories(self):
        df = pd.DataFrame(data={
            'read': [1, 0],
            'author': ['author1', 'author2'],
            'tags': ['sci-fi', 'novel, sci-fi'],
        })

        actual_categories = get_all_categories(df)
        assert isinstance(actual_categories, list)
        assert sorted(actual_categories) == ['novel', 'sci-fi']

    def test_return_ordered_list_of_categories(self):
        df = pd.DataFrame(data={
            'read': [1, 0],
            'author': ['author1', 'author2'],
            'tags': ['sci-fi', 'novel'],
        })

        actual_categories = get_all_categories(df, ordered=True)
        assert actual_categories == ['novel', 'sci-fi']

    def test_return_ordered_list_of_deduplicated_categories(self):
        df = pd.DataFrame(data={
            'read': [1, 0],
            'author': ['author1', 'author2'],
            'tags': ['sci-fi', 'novel, sci-fi'],
        })

        actual_categories = get_all_categories(df, ordered=True)
        assert actual_categories == ['novel', 'sci-fi']
