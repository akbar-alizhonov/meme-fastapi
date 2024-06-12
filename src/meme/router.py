from fastapi import APIRouter
from typing import Annotated
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.responses import Response
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from db import models
from .schemas import SMeme, SMemeReturn
from storage_service.store import client


router = APIRouter(
    prefix='/memes'
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_object_or_404(
        meme_id: int,
        db: Session,
) -> SMeme | None:
    meme = db.get(models.Meme, meme_id)

    if meme is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='такого мема не существует :('
        )

    return meme


@router.get('/')
async def get_memes(
    db: Session = Depends(get_db),
) -> Page[SMemeReturn]:
    memes = db.query(models.Meme).all()

    return paginate(memes)


@router.post('/')
async def add_new_meme(
    meme: Annotated[SMeme, Depends()],
    db: Session = Depends(get_db)
):
    data = meme.model_dump()
    object_name = client.add_image(data['image'])

    new_meme = models.Meme()
    new_meme.description = data['description']
    new_meme.image = object_name

    db.add(new_meme)
    db.flush()
    db.commit()

    return {
        'status': HTTPStatus.OK,
        'message': 'Мем успешно добавлен :)',
    }


@router.delete('/{meme_id}')
async def delete_mem(
    meme_id: int,
    db: Session = Depends(get_db)
):
    meme = db.query(models.Meme).filter(models.Meme.id == meme_id)

    client.delete_image(meme.first().image)
    meme.delete()
    db.commit()

    return {
        'status': HTTPStatus.OK,
        'message': f'Мем {meme_id} успешно удален ;)',
    }


@router.get('/{meme_id}')
async def get_meme(
    meme_id: int,
    db: Session = Depends(get_db),
):
    meme = get_object_or_404(meme_id, db)
    meme.image = client.get_image(meme.image)

    return Response(
        content=meme.image,
        media_type='image/jpg',
        status_code=HTTPStatus.OK,
        headers={'description': meme.description}
    )


@router.put('/{meme_id}')
async def update_meme(
    meme_id: int,
    new_meme: Annotated[SMeme, Depends()],
    db: Session = Depends(get_db),
):
    old_meme = get_object_or_404(meme_id, db)

    data = new_meme.model_dump()
    old_meme.description = data['description']
    old_meme.image = client.update_image(
        old_file=old_meme.image,
        new_file=data['image'],
    )
    db.flush()
    db.commit()

    return {
        'status': HTTPStatus.OK,
        'message': f'Мем {meme_id} успешно обновлен :)',
    }
