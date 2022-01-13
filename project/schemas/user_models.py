"""
Blueprints for data validation
author: Marco Aldana
"""
from pydantic import BaseModel, Field, EmailStr

from . import ResponseModel, PeeweeGetterDict


class UserRequestModel(BaseModel):
    username: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="username for user"
    )
    full_name: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="full name for user"
    )
    email: EmailStr = Field(
        ...,
        description="email for user"
    )
    password: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="user password"
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "User",
                "full_name": "User UserSon",
                "email": "user_userson@gmail.com",
                "password": "Pass1234"
            }
        }


class UserFullRequestModel(BaseModel):
    id: int = Field(
        description="Id for user"
    )
    username: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="username for user"
    )
    full_name: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="full name for user"
    )
    email: EmailStr = Field(
        ...,
        description="email for user"
    )
    password: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="user password"
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "User",
                "full_name": "User UserSon",
                "email": "user_userson@gmail.com",
                "password": "Pass1234"
            }
        }


class UserResponseModel(ResponseModel):
    id: int = Field(
        description="Id for user"
    )
    username: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="username for user"
    )
    full_name: str = Field(
        ...,
        max_length=50,
        min_length=3,
        description="full name for user"
    )
    email: EmailStr = Field(
        ...,
        description="email for user"
    )

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
