from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    from_account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    credit_id = Column(Integer, ForeignKey('credit.id'), nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
