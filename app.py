from flask import Flask
import json
import pandas as pd

from yabl.functions import get_pct_books_read, get_repartition_per_category

app = Flask(__name__)

# read-only for now, will need a database for updating info
BOOKS_LIST_FILENAME = 'books_list_2020_02_16.csv'
BOOKS = pd.read_csv(f'./data/{BOOKS_LIST_FILENAME}', header=0)


@app.route('/')
def index():
    num_books = len(BOOKS)
    pct_read = get_pct_books_read(BOOKS)
    repartition_per_category = get_repartition_per_category(BOOKS)

    ordered_repartitions = {
        key: value
        for key, value in sorted(repartition_per_category.items(), key=lambda item: item[1]['count'], reverse=True)
    }

    output = {
        'Number of books': num_books,
        'Percentage read': round(pct_read, 2),
        'Repartition per tag': ordered_repartitions,
    }

    return json.dumps(output)
