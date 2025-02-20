from pydantic import BaseModel

class BookBase(BaseModel):
    title:str
    author:str
    published_year:int
    isbn:str
    
class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id:int
    
    class config:
        orm_mode=True
        
        