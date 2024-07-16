from typing import Optional

from mongoengine import Document, EmbeddedDocument, FloatField, StringField, ListField, ReferenceField, \
    EmbeddedDocumentField
from pydantic import BaseModel, Field

from Server.models.user import User


class Hours(EmbeddedDocument):
    percentage = FloatField(required=True, default=0.0)


class HourSlotModel(BaseModel):
    percentage: Optional[float] = Field(0.0, title="Percentage", description="The percentage value for the hour slot")

# Hours model with a list of 12 blocks
# class Statistics(Document):
#     description = StringField(required=True)
#     hours = ListField(EmbeddedDocumentField(Hours), min_length=12, max_length=12)
#     user = ReferenceField(User, required=True)

# class BlockModel(BaseModel):
#     percentage: float = Field(..., title="Percentage", description="The percentage value for the block")
#
# # Pydantic model for Hours
# class HoursModel(BaseModel):
#     description: str = Field(..., title="Description", description="The description of the hours")
#     blocks: conlist(BlockModel, min_items=12, max_items=12) = Field(..., title="Blocks", description="A list of 12 blocks with percentages")
#     user_username: str = Field(..., title="User Username", description="The username of the user associated with these hours")
