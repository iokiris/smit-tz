from sqlalchemy import Column, Float, String, Integer, Date, ForeignKey, Index

from src.models.base import Base
import datetime


class Cargo(Base):
    __tablename__ = 'cargo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cargo_type = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    datetime = Column(Date, nullable=False)

    __table_args__ = (
        Index('ix_cargo_type_datetime', 'cargo_type', 'datetime', unique=True),
    )


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    cargo_id = Column(Integer, ForeignKey('cargo.id'), nullable=False)


#
#
#

