"""
For all database interaction related to users
author: Marco Aldana
"""
from fastapi import HTTPException
from pydantic import EmailStr

from project.database.models import User
from project.schemas.user_models import UserRequestModel, UserFullRequestModel
from project.database.connection import connect


class UserRepository:
    @classmethod
    def get_users_repository(cls, page, limit):
        with connect:
            users = User.select().paginate(page, limit)
            if users:
                return [user for user in users]
            else:
                raise HTTPException(status_code=404, detail=f"There is not users in database")

    @classmethod
    def get_user_by_email_repository(cls, email: EmailStr):
        with connect:
            user = User.get_or_none(User.email == email)
            if user:
                return user
            else:
                raise HTTPException(status_code=409, detail=f"There is no user whit 'email = {email}' in database")

    @classmethod
    def get_user_by_id_repository(cls, id_user: int):
        with connect:
            user = User.get_or_none(User.id == id_user)
            if not user:
                raise HTTPException(status_code=409, detail=f"There is no user whit 'id = {id_user}' in database")
            return user

    @classmethod
    def create_user_repository(cls, user_data: UserRequestModel):
        with connect:
            if User.select().where(User.username == user_data.username).first():
                raise HTTPException(status_code=409, detail='The username is in use or not valid')
            if User.select().where(User.email == user_data.email).first():
                raise HTTPException(status_code=409, detail='The mail is in use or not valid')
            hash_password = User.create_password(user_data.password)
            new_user = User.create(
                username=user_data.username,
                full_name=user_data.full_name,
                email=user_data.email,
                password=hash_password
            )
            return new_user

    @classmethod
    def edit_user_repository(cls, user_data: UserRequestModel, old_user: UserFullRequestModel):
        with connect:
            user = User.select().where(User.id == old_user.id).first()
            if not user:
                raise HTTPException(status_code=404, detail='The id does not exist')
            elif User.select().where(User.username == user_data.username).first():
                raise HTTPException(status_code=409, detail='The username is in use or not valid')
            elif User.select().where(User.email == user_data.email).first():
                raise HTTPException(status_code=409, detail='The mail is in use or not valid')

            user.username = user_data.username
            user.full_name = user_data.full_name
            user.email = user_data.email
            user.password = User.create_password(user_data.password)

            user.save()

            return user

            # user = (User.update(user_data.__dict__).where(User.id == user_data.id))
            # if not user.execute():
            #    raise HTTPException(status_code=409, detail='The user is not modified')
            # new_user = User.get_by_id(user_data.id)
            # return new_user

    @classmethod
    def delete_user_repository(cls, id_user):
        with connect:
            user = User.select().where(User.id == id_user).first()
            if not user:
                raise HTTPException(status_code=404, detail='The id does not exist')
            user.delete_instance()
            return user
