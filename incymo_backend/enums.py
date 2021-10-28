from enum import auto

from fastapi_utils.enums import CamelStrEnum


class OfferReactionType(CamelStrEnum):
    """Enumeration of a choice types reaction."""
    CLICK_PURCHASE = auto()
    CLICK_NO_PURCHASE = auto()
    DISMISS = auto()
    IGNORE = auto()


class OfferResponse(CamelStrEnum):
    """Possible variants of a reaction from game client on out suggestions."""
    UNKNOWN = 0
    CLICK_PURCHASE = 1
    CLICK_NO_PURCHASE = 2
    DISMISS = 3
    IGNORE = 4


class ItemsEnum(CamelStrEnum):
    """Our possible suggestions to the game client."""
    SWORD = 0
    HELM = 1
    BOOTS = 2
    SHIELD = 3
    BOW = 4
    HEALTH = 5
    MANA = 6
