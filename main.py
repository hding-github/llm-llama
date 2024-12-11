import os
TEST_STRING = os.getenv("TEST_STRING")
print("************** .env varilables ****************")
print(TEST_STRING)
print("version. 0.01")
print("***********************************************")

import sub_internet
tBool = sub_internet.check()

import uvicorn

import sub_llama as llm_ops
from sub_llama import user_message, response


#pip install "python-jose[crptography]"
#pip install "passlib[bcrypt]"
#pip install python-multipart

from typing import Annotated

# import fast api
#pip install "fastapi[standard]"
from fastapi import FastAPI, HTTPException, Depends
import auth
from auth import get_current_user

#needed for Lambda.
#from mangum import Mangum

#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#db_dependency = Annotated[Session, Depends(get_db)]

import time
start = time.time()

app = FastAPI()
app.include_router(auth.router)
user_dependency = Annotated[dict, Depends(get_current_user)]
# for implementation for Lambda
# handler = Mangum(app)

@app.get("/")
async def root(user: user_dependency):
    tBool = sub_internet.check()
    if tBool == True:
        print("The Internet is ready.")
    else:
        print("Could not access the Internet.")

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized.")
    return {"user": user}

# Read chat response
@app.post("/api/v1/sentiment", response_model={})
async def rephrase(user_msg: user_message, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized.")
    #return "chat_output"
    strTxt = user_msg.message
    user_id = user_msg.user_id
    date_time = user_msg.date_time
    tListRes = llm_ops.input(strTxt)
    if tListRes is None:
        raise HTTPException(status_code=404, detail="Could not similar sentences.")
    tResponse = {}
    tResponse["user_id"] = user_id
    tResponse["list_sentences"] = tListRes
    tResponse["date_time"] = date_time
    return tResponse

if __name__ == "__main__":
    #uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
    uvicorn.run("main:app", host='0.0.0.0', port=8801, reload=True)
    #uvicorn.run("main:app", host='0.0.0.0', port=80, reload=True)