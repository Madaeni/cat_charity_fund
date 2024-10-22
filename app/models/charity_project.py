from sqlalchemy import Column, String, Text

from app.models.base import ChantyProjectDonationBaseModel
from app.core.db import Base


class CharityProject(ChantyProjectDonationBaseModel, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
