from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookCreate,BookResponse
from app.crud.book import get_all_books,get_book_by_id,create_book,update_book,delete_book

router=APIRouter()

#create a new book
@router.post("/books/",response_model=BookResponse)
def create_new_book(book:BookCreate,db:Session=Depends(get_db)):
    return create_book(db,book)

#read all the books
@router.get("/books/",response_model=list[BookResponse])
def read_books(db:Session=Depends(get_db)):
    return get_all_books(db)

#read a specific boook with its id
@router.get("/books/{book_id}",response_model=BookResponse)

def read_book(book_id:int,db:Session=Depends(get_db)):
    book=get_book_by_id(db,book_id)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    return book

#update a book by its id
@router.put("books/{book_id}",response_model=BookResponse)
def update_existing_book(book_id:int,updated_data:BookCreate,db:Session=Depends(get_db)):
    book=update_book(db,book_id,updated_data)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    return book

#delete a book by its id
@router.delete("/books/{book_id}",response_model=BookResponse)

def delete_existing_book(book_id:int,db:Session=Depends(get_db)):
    book=delete_book(db,book_id)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    return {"message":"book deleted succesfully"}
