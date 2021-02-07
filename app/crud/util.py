from supermemo2 import SMTwo

from .. schemas import Card


def update_sm_two(card: Card):
    sm_two = SMTwo()
    sm_two.calc(
        card.quality,
        card.prev_easiness,
        card.prev_interval,
        card.prev_repetitions,
        card.prev_review_date
    )

    for name, value in sm_two.dict(curr=True).items():
        if name != "quality":
            setattr(card, name, value)
