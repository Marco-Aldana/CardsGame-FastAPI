from fastapi import HTTPException

from project.database.models import Card, User
from project.database.connection import connect
from project.schemas.card_models import CardRequestModel, CardGiveRequestModel


class CardRepository:
    @classmethod
    def get_cards_repository(cls, page, limit):
        with connect:
            cards = Card.select().paginate(page, limit)
            if cards:
                return [card for card in cards]
            else:
                raise HTTPException(status_code=404, detail=f"There is not cards in database")

    @classmethod
    def get_card_by_id(cls, id_card):
        with connect:
            card = Card.get_or_none(Card.id == id_card)
            if not card:
                raise HTTPException(status_code=404, detail=f"There is no card with 'id= {id_card}' in database")
            return card

    @classmethod
    def create_cards_repository(cls, card: CardRequestModel):
        with connect:
            if not User.select().where(User.id == card.owner).first():
                raise HTTPException(status_code=404, detail='The owner is not valid or does not exists')
            card = Card.create(
                name=card.name,
                attack=card.attack,
                defense=card.defense,
                type=card.type,
                civilization=card.civilization,
                description=card.description,
                image=card.image,
                owner=card.owner
            )
            return card

    @classmethod
    def give_card_repository(cls, edit_request_card: CardGiveRequestModel, user):
        with connect:
            card = Card.select().where(Card.id == edit_request_card.id).first()
            owner=card.owner.__dict__.get("__data__").get("id")
            if not card:
                raise HTTPException(status_code=404, detail='The card is not valid or does not exists')
            if owner != user.id:
                raise HTTPException(status_code=401, detail="You are not able to gift this card")
            if owner==edit_request_card.owner:
                raise HTTPException(status_code=409, detail="You are not able to gift this card to yourself")
            if not User.select().where(User.id == edit_request_card.owner).first():
                raise HTTPException(status_code=404, detail='The target owner is not valid or does not exists')

            card.owner=edit_request_card.owner

            card.save()

            return card
