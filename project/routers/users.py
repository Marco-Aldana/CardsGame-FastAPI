from typing import List

from fastapi import APIRouter, Path, Body, Depends, HTTPException

from testing.example_constants_swagger import ID_EXAMPLE
from .common import get_current_user
from ..database.models import User
from ..repository.user_repository import UserRepository
from ..schemas.user_models import UserResponseModel, UserRequestModel

router = APIRouter(prefix='/users')


# USER endpoints--------------------------------------------------------------------------------------------------------
@router.get('', response_model=List[UserResponseModel])
async def get_users(page: int = 1, limit: int = 5):
    response: List[UserResponseModel] = UserRepository.get_users_repository(page, limit)
    return response


@router.get('/{id_user}', response_model=UserResponseModel)
async def get_user_by_id(
        id_user: int = Path(
            ...,
            example=ID_EXAMPLE
        )):
    response: UserResponseModel = UserRepository.get_user_by_id_repository(id_user)
    return response


@router.get('/profile/', response_model=UserResponseModel)
async def get_profile(user: User = Depends(get_current_user)):
    response: UserResponseModel = UserRepository.get_user_by_id_repository(user.id)
    return response


@router.post('', response_model=UserResponseModel)
async def create_user(
        user: UserRequestModel = Body(
            ...
        )):
    response: UserResponseModel = UserRepository.create_user_repository(user)
    return response


@router.put('/profile/', response_model=UserResponseModel)
async def edit_user(
        user_data: UserRequestModel = Body(
            ...
        ),
        user: User = Depends(get_current_user)
):
    if user:
        response: UserResponseModel = UserRepository.edit_user_repository(user_data, user)
    else:
        raise HTTPException(404, "User does not exist")
    return response


@router.delete('/profile/', response_model=UserResponseModel)
async def delete_user(
        user: User = Depends(get_current_user)
):
    if user:
        response: UserResponseModel = UserRepository.delete_user_repository(user.id)
    else:
        raise HTTPException(404, "User does not exist")
    return response
