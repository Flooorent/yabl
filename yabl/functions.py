from collections import namedtuple

READ = 1
UNREAD = 0

Book = namedtuple('Book', ['title', 'author', 'tags'])
Book.__doc__ += 'Book metadata'
Book.title.__doc__ = "book's title, str"
Book.author.__doc__ = "book's author, str"
Book.tags.__doc__ = "book's tags, str, if multiple tags then comma-separated str"


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


# TODO: update function with category
def get_random_unread_book(books, category='Any category'):
    """Pick one unread book at random.

    :param books: dataframe containing all books (read and unread)
    :type books: pandas.DataFrame
    :param category: category to choose from. If passed 'Any category', all categories will be taken into account.
    Default is 'Any category'.
    :type category: str

    :return: a random unread book. If there are no unread books, return None.
    :rtype: Book or None if no unread books
    """
    if not isinstance(category, str):
        raise TypeError("Parameter 'category' must be a string")

    unread_books = books[books['read'] == 0]

    if category != 'Any category':
        # TODO: ça revient plusieurs fois à travers différentes fonctions, le cleaner
        unread_books['clean_tags'] = unread_books['tags'].apply(lambda tags: [tag.strip() for tag in tags.split(',')])
        unread_books = unread_books[unread_books['clean_tags'].apply(lambda tags: category in tags)]

    if not unread_books.empty:
        random_book = unread_books.sample(1).fillna('').to_dict(orient='list')
        return Book(title=random_book['title'][0], author=random_book['author'][0], tags=random_book['tags'][0])


def get_all_categories(books, ordered=False):
    """Get all categories from all books.

    :param books: dataframe containing all books (read and unread)
    :type books: pandas.DataFrame
    :param ordered: True if output categories must be ordered, False otherwise. False by default.
    :type ordered: bool
    :return: all categories
    :rtype: list
    """
    if books.empty:
        return []

    nested_tags = books['tags'].fillna('').apply(lambda tags: [tag.strip() for tag in tags.split(',')]).to_list()
    unique_tags = list(set([tag for tags in nested_tags for tag in tags if tag != '']))

    if ordered:
        unique_tags.sort()

    return unique_tags
