from typing import Optional, List
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Association table for many-to-many relationship between User and Group
user_group = Table('user_group',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    address_id: Mapped[int] = mapped_column(ForeignKey('address.id'))
    address: Mapped[Optional['Address']] = relationship('Address', back_populates='user', uselist=False)
    groups: Mapped[List['Group']] = relationship('Group', secondary=user_group, back_populates='users')

    modified: Mapped[datetime] = mapped_column(onupdate=func.now())
    created: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[List['User']] = relationship('User', secondary=user_group, back_populates='groups')

    def __repr__(self):
        return f"Group(id={self.id!r}, name={self.name!r})"

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[Optional[str]] = mapped_column(nullable=False)
    city: Mapped[Optional[str]] = mapped_column(nullable=False)
    postal_code: Mapped[Optional[str]] = mapped_column(nullable=False)
    country: Mapped[Optional[str]] = mapped_column(nullable=False)
    user: Mapped[Optional['User']] = relationship('User', back_populates='address')

    def __repr__(self):
        return f"Address(id={self.id!r}, street={self.street!r}, city={self.city!r}, postal_code={self.postal_code!r}, country={self.country!r})"

# Association table for many-to-many relationship between User and Group
# user_group = db.Table('user_group',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
# )

# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255))
#     last_name = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     is_active = db.Column(db.Boolean, default=True)
#     is_staff = db.Column(db.Boolean, default=False)
#     is_superuser = db.Column(db.Boolean, default=False)
#     address = db.relationship('Address', uselist=False, back_populates='user', cascade='all, delete-orphan')
#     groups = db.relationship('Group', secondary=user_group, back_populates='users')

#     modified = db.Column(db.DateTime, onupdate=db.func.now())
#     created = db.Column(db.DateTime, server_default=db.func.now())

#     def __repr__(self):
#         return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

# class Group(db.Model):
#     __tablename__ = "group"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     users = db.relationship('User', secondary=user_group, back_populates='groups')

#     def __repr__(self):
#         return f"Group(id={self.id!r}, name={self.name!r})"

# class Address(db.Model):
#     __tablename__ = "address"
#     id = db.Column(db.Integer, primary_key=True)
#     street = db.Column(db.String(255))
#     city = db.Column(db.String(255))
#     postal_code = db.Column(db.String(255))
#     country = db.Column(db.String(255))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', back_populates='address')

#     def __repr__(self):
#         return f"Address(id={self.id!r}, street={self.street!r}, city={self.city!r}, postal_code={self.postal_code!r}, country={self.country!r})"