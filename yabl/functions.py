READ = 1
UNREAD = 0


def get_pct_books_read(books):
    if books.empty:
        raise ValueError("books DataFrame can't be empty")

    reads_to_counts = books['read'].value_counts().to_dict()
    num_read = reads_to_counts.get(READ, 0)
    num_unread = reads_to_counts.get(UNREAD, 0)
    return num_read / (num_read + num_unread)


def get_repartition_per_category(books):
    if books.empty:
        raise ValueError("books DataFrame can't be empty")

    books['clean_tags'] = books['tags'].apply(lambda tags: [tag.strip() for tag in tags.split(',')])
    exploded_books = books.explode('clean_tags')[['read', 'clean_tags']]
    tags_and_counts = exploded_books.groupby('clean_tags').agg({'read': ['sum', 'count']})['read'].reset_index()
    tags_and_counts['pct'] = tags_and_counts['sum'] / tags_and_counts['count']
    tags_and_counts['pct'] = tags_and_counts['pct'].apply(lambda pct: round(pct, 2))
    tags_and_counts.drop('sum', axis=1, inplace=True)

    return tags_and_counts.set_index('clean_tags').to_dict(orient='index')
