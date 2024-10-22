from sqlalchemy import Column, Integer, Text, ForeignKey

from app.models.base import ChantyProjectDonationBaseModel
from app.core.db import Base


class Donation(ChantyProjectDonationBaseModel, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
