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
    pass
