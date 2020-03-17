from collections import namedtuple

READ = 1
UNREAD = 0

Book = namedtuple('Book', ['title', 'author'])


def get_pct_books_read(books):
    """Compute the percentage fo books read.

    :param books: dataframe containing all books (read and unread)
    :type books: pandas.DataFrame
    :return: the percentage of books read
    :rtype: float
    """
    if books.empty:
        raise ValueError("books DataFrame can't be empty")

    reads_to_counts = books['read'].value_counts().to_dict()
    num_read = reads_to_counts.get(READ, 0)
    num_unread = reads_to_counts.get(UNREAD, 0)
    return num_read / (num_read + num_unread)


def get_repartition_per_category(books):
    """Compute for each category of books the number of all books (read and unread) and the percentage of books read.

    :param books: dataframe containing all books (read and unread)
    :type books: pandas.DataFrame
    :return: a dict of the form
    {
        category1: {
            'count': count1,
            'pct': pct1,
        },
        ...
    }
    :rtype: dict
    """
    if books.empty:
        raise ValueError("books DataFrame can't be empty")

    books['clean_tags'] = books['tags'].apply(lambda tags: [tag.strip() for tag in tags.split(',')])
    exploded_books = books.explode('clean_tags')[['read', 'clean_tags']]
    tags_and_counts = exploded_books.groupby('clean_tags').agg({'read': ['sum', 'count']})['read'].reset_index()
    tags_and_counts['pct'] = tags_and_counts['sum'] / tags_and_counts['count']
    tags_and_counts['pct'] = tags_and_counts['pct'].apply(lambda pct: round(pct, 2))
    tags_and_counts.drop('sum', axis=1, inplace=True)

    return tags_and_counts.set_index('clean_tags').to_dict(orient='index')


def get_random_unread_book(books):
    """Pick one unread book at random.

    :param books: dataframe containing all books (read and unread)
    :type books: pandas.DataFrame
    :return: a random unread book. If there are no unread books, return None.
    :rtype: Book or None if no unread books
    """
    unread_books = books[books['read'] == 0]

    if not unread_books.empty:
        random_book = unread_books.sample(1).fillna('').to_dict(orient='list')
        return Book(title=random_book['title'][0], author=random_book['author'][0])
