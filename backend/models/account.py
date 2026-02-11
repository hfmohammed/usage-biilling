from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from datetime import datetime
from database import Base
from models.__init__ import new_id


class AccountDB(Base):
    """
    AccountDB model represents a user's account in the system.
    """

    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True, default=new_id)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "currency": self.currency,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
