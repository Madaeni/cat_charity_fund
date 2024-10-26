from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, DateTime, CheckConstraint


class ChantyProjectDonationBaseModel:
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.now)
    close_date = Column(DateTime, index=True, nullable=True)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='valid_full_amount'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='valid_invested_amount'
        )
    )
