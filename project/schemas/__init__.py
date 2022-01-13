import peewee
from pydantic import BaseModel
from typing import Any

from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        response = getattr(self._obj, key, default)
        if isinstance(response, peewee.ModelSelect):
            return list(response)
        return response


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
