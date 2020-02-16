from flask import Flask
import json
import pandas as pd

from yabl.functions import get_pct_books_read

app = Flask(__name__)

# read-only for now, will need a database for updating info
BOOKS_LIST_FILENAME = 'books_list_2020_02_16.csv'
BOOKS = pd.read_csv(f'./data/{BOOKS_LIST_FILENAME}', header=0)


@app.route('/')
def index():
    num_books = len(BOOKS)
    pct_read = get_pct_books_read(BOOKS)

    output = {
        'Number of books': num_books,
        'Percentage read': round(pct_read, 2)
    }

    return json.dumps(output)
