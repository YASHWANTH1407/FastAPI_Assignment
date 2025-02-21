from sqlalchemy import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth import create_access_token,verify_password,hash_password

router=APIRouter()

#register page
@router.post("/register")
def register(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.username==user.username).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Username already registered")
    new_user=User(username=user.username,password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User registered successfully"}

#login page
@router.post("/login")
def loginn(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==form_data.username).first()
    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
    token=create_access_token(data={"sub":user.username})
    return {"access_token":token,"token_type":"bearer"}


    