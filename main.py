from fastapi import FastAPI

from app.appUser import user_router

api = FastAPI(title="FundooNotes", )
api.include_router(user_router, prefix='/user', tags=['User'])
