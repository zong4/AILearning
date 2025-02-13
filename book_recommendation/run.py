# import libraries (you may add additional imports but you may not have to)
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import csv
import json
from sklearn.preprocessing import StandardScaler
import logging
import datetime

# set up logging
filename = './book_recommendation/log' + str(datetime.datetime.now()) + '.log'
logging.basicConfig(filename=filename, level=logging.INFO)

# get data files
# !wget https://cdn.freecodecamp.org/project-data/books/book-crossings.zip
# !unzip book-crossings.zip
books_filename = './book_recommendation/book-crossings/BX-Books.csv'
ratings_filename = './book_recommendation/book-crossings/BX-Book-Ratings.csv'
users_filename = './book_recommendation/book-crossings/BX-Users.csv'

# import csv data into dataframes
df_books = pd.read_csv(
    books_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author', 'year', 'publisher'],
    usecols=['isbn', 'title', 'author', 'year', 'publisher'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str', 'year': 'str', 'publisher': 'str'},
    quoting=csv.QUOTE_ALL
    )

df_ratings = pd.read_csv(
    ratings_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'},
    quoting=csv.QUOTE_ALL,
    )

df_users = pd.read_csv(
    users_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'location', 'age'],
    usecols=['user', 'location', 'age'],
    dtype={'user': 'int32', 'location': 'str', 'age': 'float32'},
    quoting=csv.QUOTE_ALL
    )

# draw a bar chart of the number of books rated by each user
ratings_per_user = df_ratings.groupby('user')['rating'].count()
ratings_per_book = df_ratings.groupby('isbn')['rating'].count()
logging.info("The distribution of ratings per book: ")
logging.info(ratings_per_book.describe())

# average rating and number of ratings for each book
average_rating = df_ratings.groupby('isbn')['rating'].mean()
rating_count = df_ratings.groupby('isbn')['rating'].count()
df_ratings_avg = pd.DataFrame({'isbn': average_rating.index, 'avg_rating': average_rating.values, 'rating_count': rating_count.values})

# process df_books
df_books = df_books[df_books['year'].str.isnumeric()]
df_books['year'] = df_books['year'].astype(int)
df_books = df_books.dropna()

# One-hot encoding
# df_books = pd.get_dummies(df_books, columns=['author'])
# df_books = pd.get_dummies(df_books, columns=['publisher'])

# extract extra features
extra_features = df_books.drop(columns=['title', 'publisher', 'author'])
logging.info("Extra features: ")
logging.info(extra_features)

# join the dataframes
df = df_books.set_index('isbn').join(df_ratings.set_index('isbn'))
df = df.groupby('isbn').filter(lambda x: len(x) >= 100)
user_book_matrix = df.pivot_table(index='isbn', columns='user', values='rating').fillna(0)
logging.info("User book matrix: ")
logging.info(user_book_matrix)

# concat by isbn
extra_features.set_index('isbn', inplace=True)
combined_data = pd.concat([user_book_matrix, extra_features], axis=1)
combined_data = combined_data.dropna()
combined_data = combined_data[combined_data['year'] != 0]
logging.info("Combined data: ")
logging.info(combined_data)

# train the knn model
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
model_knn.fit(combined_data.values)

# function to return recommended books - this will be tested
def get_recommends(book = ""):
    # get the isbn of the book
    isbn_index = df_books[df_books['title'] == book]['isbn'].values[0]

    # get the index of the book in the combined data
    logging.info("Book: " + book)
    logging.info("ISBN index: ")
    if isbn_index not in combined_data.index:
        logging.info("Book not found.")
        return []
    book_index = combined_data.index.get_loc(isbn_index)

    distances, indices = model_knn.kneighbors(combined_data.iloc[book_index].values.reshape(1, -1), n_neighbors=5)

    # the format of the recommended books
    # {
    #     book:
    #     {
    #         [similar_book_1_isbn, similar_book_1_title]: distance_1,
    #         [similar_book_2_isbn, similar_book_2_title]: distance_2,
    #         [similar_book_3_isbn, similar_book_3_title]: distance_3,
    #         [similar_book_4_isbn, similar_book_4_title]: distance_4,
    #         [similar_book_5_isbn, similar_book_5_title]: distance_5
    #     }
    # }
    recommended_books = {}
    for i in range(1, len(indices[0])):
        recommended_book_isbn = combined_data.iloc[indices[0][i]].name
        recommended_book_title = df_books.loc[df_books['isbn'] == recommended_book_isbn, 'title'].values[0]
        recommended_books[recommended_book_isbn + " "+ recommended_book_title] = distances[0][i]

    return recommended_books

books = get_recommends("Where the Heart Is (Oprah's Book Club (Paperback))")
logging.info("Recommended books: ")
logging.info(books)
print(json.dumps(books, indent=4))

#     recommended_books = ["I'll Be Seeing You", 'The Weight of Water', 'The Surgeon', 'I Know This Much Is True']
#     recommended_books_dist = [0.8, 0.77, 0.77, 0.77]