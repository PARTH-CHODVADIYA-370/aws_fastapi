from pydantic import BaseModel


class Posts(BaseModel):
    TITLE: str
    DESCRIPTION: str
    TAG: str
    FEATURED: str
    STATUS: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {
            "example": {
                "TITLE": "Slow-cooker Stuffed Peppers",
                "DESCRIPTION": "When someone asks you to make a muscle, chances are you don’t flex your traps or rise onto your toes to show off your calves. You're going to roll up your sleeves and flex your biceps, inviting onlookers to your own personal gun show.",
                "TAG": "TIPS",
                "FEATURED": "YES",
                "STATUS": "ACTIVE",
                "IMAGE": "BASE64 PATH",
            }
        }
