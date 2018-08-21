import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://paqubihkgzolaw:eb799f12a49889a8db4179144030e86e7920414e33e08503a78a8a02598caeb0@ec2-54-235-242-63.compute-1.amazonaws.com:5432/dcsd1tqompgjg2")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added '{title}' by {author}, published {year} with ISBN number {isbn} to database.")
    db.commit()

if __name__ == "__main__":
    main()
