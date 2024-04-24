from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from Deps.deps import get_db
from typing import Annotated,Optional
from fastapi.encoders import jsonable_encoder


from Models.news_models import (
    NewsCreate,
    News
    
)
news_router =APIRouter(tags=["Laundrex_News"])

@news_router.post("/news")
async def create_news(news:NewsCreate,db:
Session=Depends(get_db)):
    existing_news = db.query(News).filter(News.title == news.title).first()
    if existing_news:
        raise HTTPException(status_code=400, detail="News already exists")
    new_news = News(**news.model_dump())
    db.add(new_news)
    db.commit()

    response ={"message": "success", "data":jsonable_encoder(new_news)} 

    return JSONResponse(status_code = 201, content = response)

    # return News

@news_router.get("/news/{news_id}")
async def get_news(news_id:int,session:Session=Depends(get_db)):
    my_news=session.get(News,news_id)
    if not my_news:
        raise HTTPException(status_code=404,detail="News not found")
    
    response ={"message": "success", "data":jsonable_encoder(my_news)} 

    return response

@news_router.put("/news/{news_id}")
def update_news(news_id: int, news: News, session: Session = Depends(get_db)):
    db_news = session.get(News, news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    db_news.title = news.title
    db_news.description = news.description
    session.add(db_news)
    session.commit()
    return db_news
        


@news_router.patch("/news{news_id}")
def delete_news(news_id: int, session: Session = Depends(get_db)):
    news = session.get(News, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    session.delete(news)
    session.commit()
    return news
    


