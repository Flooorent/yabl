from flask import Flask, render_template
import json
import pandas as pd

from yabl.functions import (
    get_pct_books_read,
    get_random_unread_book,
    get_repartition_per_category,
)

app = Flask(__name__)

# read-only for now, will need a database for updating info
BOOKS_LIST_FILENAME = 'books_list_2020_02_16.csv'
BOOKS = pd.read_csv(f'./data/{BOOKS_LIST_FILENAME}', header=0)


@app.route('/')
def index():
    template_file = 'unread_books.html'

    if BOOKS.empty:
        return render_template(template_file, no_books=True)

    num_books = len(BOOKS)
    pct_read = get_pct_books_read(BOOKS)
    repartition_per_category = get_repartition_per_category(BOOKS)

    ordered_repartitions = {
        key: value
        for key, value in sorted(repartition_per_category.items(), key=lambda item: item[1]['count'], reverse=True)
    }

    return render_template(
        template_file,
        no_books=False,
        num_books=num_books,
        pct_read=int(round(pct_read, 2) * 100),
        ordered_repartitions=ordered_repartitions,
    )


@app.route('/random')
def pick_at_random():
    template_file = 'random_picker.html'
    random_book = get_random_unread_book(BOOKS)

    if random_book:
        return render_template(template_file, title=random_book.title, author=random_book.author, no_unread_books=False)
    else:
        return render_template(template_file, no_unread_books=True)
