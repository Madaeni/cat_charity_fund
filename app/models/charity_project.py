from sqlalchemy import Column, String, Text

from app.models.base import ChantyProjectDonationBaseModel
from app.core.db import Base

from core.constants import PROJECT_NAME_MAX_LENGTH


class CharityProject(ChantyProjectDonationBaseModel, Base):
    name = Column(
        String(PROJECT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    description = Column(Text, nullable=False)
