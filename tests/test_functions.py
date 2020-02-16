import pandas as pd
import pytest

from yabl.functions import get_pct_books_read


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
        assert False
