import os
from contextlib import contextmanager
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "boutique.sqlite")

Base = declarative_base()


class InstallationDates(Base):
    __tablename__ = "InstallationDates"
    package_name = Column('packageName', String(32), primary_key=True)
    package_type = Column("packageType", String(10),  nullable=False)  # curated, snap, apt ( PackageKit )
    installation_datetime = Column("installationDatetime", DateTime(timezone=True), default=datetime.now())


engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)

SESSION_CLASS = sessionmaker(bind=engine)


@contextmanager
def db_session():
    session = SESSION_CLASS()
    try:
        yield session
    finally:
        session.commit()
