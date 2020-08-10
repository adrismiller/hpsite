from models import * 
import csv

def main(): 
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader: 
        b = Book(isbn=isbn, title=title, author=author, datep=year)
        db.session.add(b)

    db.session.commit()
if __name__ == "__main__":
    with app.app_context(): 
        main()