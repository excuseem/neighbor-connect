from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo = True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    bio = Column(String, nullable=False)
    profile_picture = Column(String, nullable=False)
    password_hash = Column(String(128))

    def __init__(self, fullname, telephone, email, country, city, street, bio, profile_picture):
        self.fullname = fullname
        self.telephone = telephone
        self.email = email
        self.country = country
        self.city = city
        self.street = street
        self.bio = bio
        self.profile_picture = profile_picture
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    place = Column(String, nullable=False)
    offer = Column(String, nullable=False)
    tags = Table('tags', Base.metadata,
        Column('offer_id', Integer, ForeignKey('offers.id')),
        Column('tag', String, nullable=False)
    )


class Incident(Base):
    __tablename__ = 'incidents'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    picture = Column(String)


Session = sessionmaker(bind=engine)
db_session = Session()

Base.metadata.create_all(bind=engine)
