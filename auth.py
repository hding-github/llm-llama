
import os
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHEM = os.getenv("JWT_ALGORITHEM")
JWT_USER_CREATION_KEY = os.getenv("JWT_USER_CREATION_KEY")
JWT_EXPIRES_DELTA = os.getenv("JWT_EXPIRES_DELTA")

MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")



from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
#from sqlalchemy.orm import Session
from starlette import status
#from database import SessionLocal

#pip install passlib
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

#pip install python-jose
from jose import jwt, JWTError

#pip install motor
from motor.motor_asyncio import AsyncIOMotorClient

import mongodb as db
import hashlib
import sub_internet
import time

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(email_address: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email_address, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHEM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    print("********************** get_current_user **********************")
    testPoint = 0
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHEM])
        user_email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if user_email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized.")
        return {"user_email": user_email, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error: Unable to process JWT.")
    
ser_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)



class CreateUserRequest(BaseModel):
    email_address: str
    password: str
    creation_key: str

class Token(BaseModel):
    access_token: str
    token_type: str
    #expires_in: int

#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#db_dependency = Annotated[Session, Depends(get_db)]


# method for start the MongoDb Connection
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    #Database name
    app.mongodb = app.mongodb_client.get_database("db_pipelines")
    print("MongoDB connected.")

# method to close the database connection
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/token", response_model=Token)
def login_for_access_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print("********************** login_for_access_token **********************")
    mMongodb = db.MongoDB_Atlas_Client()
    user = authenticate_user(form_data.username, form_data.password, mMongodb)
    print("********** authenticate user ********************")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    
    user_email = user["email_address"]
    user_id = str(user["_id"])

    if str(type(user_id)) != str(type(int(1))):
        user_id = 0

    token = create_access_token(user_email, user_id, timedelta(minutes=20))
    return Token(access_token=token, token_type="bearer")

def hide_key_then_print(tD, tKey):
    tD0 = tD.copy()
    if tKey in tD0:
        tD0[tKey]= "******"
        print(tD0)
        return True
    else:
        print("Error: The dictionary does not contain the key.")
        return False

def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()

def verify_password(strPassword, HashedPassword):
    tHashedPassword = hash_password(strPassword)
    if tHashedPassword == HashedPassword:
        return True
    else:
        return False
    
def authenticate_user(user_email: str, password: str, mMongodb):
    print("********************** authenticate_user **********************")
    tBool = sub_internet.check()
    if tBool == True:
        print("The Internet is ready.")
    else:
        print("Could not access the Internet.")

    #user = db.query(users).filter(users.email == user_email).first()
    strTable = "users"
    strItem = "email_address"
    strItemToFind = user_email

    #tTitle = "Ecommerce Catalogue System"
    #tDB = db.MongoDB_Atlas_Client()
    #filter = {"title": tTitle}
    #collection_name = "agents"
    #agent = tDB.find_one(collection_name, filter)
    #print(agent)

    collection_name = "users"
    filter = {"email_address": user_email}

    print("*** mMongodb.find_one start ***********")
    time_start = time.time()
    user = mMongodb.find_one(collection_name, filter)
    time_end = time.time()
    print(time_end - time_start)
    print("*** mMongodb.find_one end ***********")
    if user is None:
        raise HTTPException(status_code=404, detail="Could not find the user.")
    #user_print = user.copy()
    #user_print["hashed_password"] = "******"
    hide_key_then_print(user, "hashed_password")

    strHashedData= user["hashed_password"]
    tResultBool = verify_password(password,strHashedData)
    if not tResultBool:
        return None
    return user

