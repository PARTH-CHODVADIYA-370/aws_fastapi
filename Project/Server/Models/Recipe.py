from pydantic import BaseModel


class Recipe(BaseModel):
    TITLE: str
    DESCRIPTION: str
    INGREDIENTS: str
    DIRECTIONS: str
    CATEGORY: str
    PRICE: str
    CALORIES: int
    CARBS: int
    PROTEIN: int
    FAT: int
    SERVINGS: int
    TOTAL_TIME: int
    FEATURED: str
    STATUS: str
    IMAGE: bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {
            "example": {
                "TITLE": "Slow-cooker Stuffed Peppers",
                "DESCRIPTION": "When someone asks you to make a muscle, chances are you don’t flex your traps or rise onto your toes to show off your calves. You're going to roll up your sleeves and flex your biceps, inviting onlookers to your own personal gun show.",
                "INGREDIENTS": "Agg, Apple and Orage",
                "DIRECTIONS": "1 tea Spoon",
                "CATEGORY": "Low Cholesterol",
                "PRICE": "Free",
                "CALORIES": 2200,
                "CARBS": 500,
                "PROTEIN": 200,
                "FAT": 22,
                "SERVINGS": 2,
                "TOTAL_TIME": 43,
                "FEATURED": "YES",
                "STATUS": "ACTIVE",
                "IMAGE": "BASE64 PATH",
            }
        }
