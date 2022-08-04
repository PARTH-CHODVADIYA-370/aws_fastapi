from pydantic import BaseModel, HttpUrl


class Tags(BaseModel):
    TITLE: str
    # IMAGE:  Optional[ImageSchema] = None
    class Config:
        schema_extra = {
            "example": {
                "TITLE": "Fitness",
            }
        }
