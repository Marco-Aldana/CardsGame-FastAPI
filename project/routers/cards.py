from fastapi import APIRouter, Body, Path, Depends, Query
from typing import List

from testing.example_constants_swagger import ID_EXAMPLE
from .common import get_current_user
from ..database.models import User
from ..repository.card_repository import CardRepository
from ..schemas.card_models import CardRequestModel, CardResponseModel, CardGiveRequestModel

router = APIRouter(prefix='/cards')


@router.get('', response_model=List[CardResponseModel])
async def get_cards(page: int = 1, limit: int = 5):
    response: List[CardResponseModel] = CardRepository.get_cards_repository(page, limit)
    return response


@router.get('/{id_card}', response_model=CardResponseModel)
async def get_card_by_id(
        id_card: int = Path(
            ...,
            example=ID_EXAMPLE
        )):
    response: CardResponseModel = CardRepository.get_card_by_id(id_card)
    return response


@router.post('', response_model=CardResponseModel)
async def create_card(card: CardRequestModel = Body(...)):
    response: CardResponseModel = CardRepository.create_cards_repository(card)
    return response


@router.put('/give/', response_model=CardResponseModel)
async def give_card(
        card_data: CardGiveRequestModel = Body(
            ...
        ),
        user: User = Depends(get_current_user)
):
    response:CardResponseModel=CardRepository.give_card_repository(card_data,user)
    return response
