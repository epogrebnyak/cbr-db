"""
SQLAlchemy models for SQLite database.
"""
from sqlalchemy import Column, String, Date, Integer, BigInteger, SmallInteger, UniqueConstraint, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from cbr_db.conf import settings


Base = declarative_base()
engine = create_engine('sqlite:///' + settings.DB_SQLITE)
Session = sessionmaker()
Session.configure(bind=engine)


class Source(Base):
    """
    Data sources (dbf, txt files)
    """
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    form = Column(Integer)
    source = Column(String(255), unique=True)


class F101(Base):
    __tablename__ = 'f101'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey(Source.id, ondelete='CASCADE'))
    dt = Column(Date)
    regn = Column(Integer)
    conto = Column(Integer)
    a_p = Column(SmallInteger)
    ir = Column(BigInteger)
    iv = Column(BigInteger)
    itogo = Column(BigInteger)
    has_iv = Column(SmallInteger)

    __table_args__ = (
        UniqueConstraint('dt', 'regn', 'conto'),
    )


class F102(Base):
    __tablename__ = 'f102'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey(Source.id, ondelete='CASCADE'))
    regn = Column(Integer)
    quart = Column(SmallInteger)
    year = Column(SmallInteger)
    code = Column(String(10))
    ir = Column(BigInteger)
    iv = Column(BigInteger)
    itogo = Column(BigInteger)
    has_iv = Column(SmallInteger)

    __table_args__ = (
        UniqueConstraint('quart', 'year', 'regn', 'code'),
    )
