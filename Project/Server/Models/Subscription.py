from pydantic import BaseModel


class Subscriptions(BaseModel):
    NAME: str
    PRICE: int
    DURATION: str
    DESCRIPTION: str
    STATUS: str
    IMAGE: str

    class Config:
        schema_extra = {
            "example": {
                "NAME": "NORMAL",
                "PRICE": 299,
                "DURATION": "3 MONTHS",
                "DESCRIPTION": "This is a normal subscription",
                "STATUS": "ACTIVE",
                "IMAGE": "BASE64 PATH",
            }
        }
