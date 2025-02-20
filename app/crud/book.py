from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

def get_all_books(db:Session):
    return db.query(Book).all()

def get_book_by_id(db:Session,book_id:int):
    return db.query(Book).filter(Book.id==book_id).first()
#create a new book
def create_book(db:Session,book:BookCreate):
    db_book=Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

#updating a book by its id
def update_book(db:Session,book_id:int,updated_data:BookCreate):
    db_book=db.query(Book).filter(Book.id==book_id).first()
    if not db_book:
        return None
    
    db_book.title=updated_data.title
    db_book.author=updated_data.author
    db_book.published_year=updated_data.published_year
    db_book.isbn=updated_data.isbn
    
    db.commit()
    db.refresh(db_book)
    return db_book


#deleting a book by its id
def delete_book(db:Session,book_id:int):
    db_book=db.query(Book).filter(Book.id==book_id).first()
    if not db_book:
        return None
    
    db.delete(db_book)
    db.commit()
    return db_book


