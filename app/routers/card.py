from fastapi import APIRouter

from .. schemas.card import Card


router = APIRouter()


@router.get('/{card_id}')
def read_card(card_id: int):
    return {'Hello': 'Cards'}


@router.post('/')
def create_card(card: Card):
    return {'Hello': 'Cards'}


@router.put('/{card_id}')
def update_card(card: Card, card_id: int):
    return {'Hello': 'Cards'}


@router.delete('/{card_id}')
def delete_card(card_id: int):
    return {'Hello': 'Cards'}
