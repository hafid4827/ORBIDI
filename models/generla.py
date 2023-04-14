from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

from models.create_table_connection import psql_connect


Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)
    website = Column(String)
    errors = relationship("Error", secondary="contact_error")


class Error(Base):
    __tablename__ = 'error'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ContactError(Base):
    __tablename__ = 'contact_error'

    contact_id = Column(Integer, ForeignKey('contacts.id'), primary_key=True)
    error_id = Column(Integer, ForeignKey('error.id'), primary_key=True)


def session_db():
    # Base parameter is added as an object psql_connect(Base=Base)
    session_interactive = psql_connect()
    return session_interactive
