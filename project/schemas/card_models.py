"""
Blueprints for data validation
author: Marco Aldana
"""
from typing import Optional

from pydantic import BaseModel, Field

from . import ResponseModel, PeeweeGetterDict


# TODO create a enum function to list the civilizations available
from ..schemas.user_models import UserResponseModel


class CardRequestModel(BaseModel):
    name: str = Field(
        ...,
        max_length=50,
        min_length=2,
        description="username for card"
    )
    attack: int = Field(
        ...,
        description="card attack"
    )
    defense: int = Field(
        ...,
        description="card defense"
    )
    type: str = Field(
        ...,
        description="type of card"
    )
    civilization: str = Field(
        ...,
        max_length=50,
        min_length=2,
        description="civilization to belongs"
    )
    description: str = Field(
        ...,
        max_length=50,
        min_length=5,
        description="description of the card"
    )
    image: str = Field(
        ...,
        description="image of the card"
    )
    owner: int=Field(
        description="The owner of this card"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Zeus",
                "attack": 11,
                "defense": 11,
                "type": "God",
                "civilization": "Grecian",
                "description": "Father of thunders",
                "image": "no image yet",
                "owner": 1
            }
        }

class CardGiveRequestModel(BaseModel):
    id: int = Field(
        description="Id for card"
    )
    owner: int=Field(
        description="The owner of this card"
    )

    class Config:
        schema_extra = {
            "example": {
                "id":1,
                "owner": 1
            }
        }

class CardResponseModel(ResponseModel):
    id: int = Field(
        description="Id for card"
    )

    name: str = Field(
        ...,
        max_length=50,
        min_length=2,
        description="username for card"
    )
    attack: int = Field(
        ...,
        description="card attack"
    )
    defense: int = Field(
        ...,
        description="card defense"
    )
    type: str = Field(
        ...,
        description="type of card"
    )
    civilization: str = Field(
        ...,
        max_length=50,
        min_length=2,
        description="civilization to belongs"
    )
    description: str = Field(
        ...,
        max_length=50,
        min_length=5,
        description="description of the card"
    )
    image: str = Field(
        ...,
        description="image of the card"
    )
    owner: UserResponseModel

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
