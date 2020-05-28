from models import * 
import csv

def main(): 
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader: 
        b = Book(isbn=isbn, title=title, author=author, datep=year)
        db.session.add(b)
        
        #print(f"isbn is {isbn} title is {title} author is {author} year is {year}")
    db.session.commit()
if __name__ == "__main__":
    with app.app_context(): 
        main()