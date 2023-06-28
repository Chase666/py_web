import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db, app
from users_policy import UsersPolicy

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer)
    phash = db.Column(db.String(200), nullable=False)


    def set_password(self, password):
        self.phash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.phash, password)

    @property
    def is_admin(self):
        return self.role_id == app.config['ADMINROLE_ID']

    @property
    def is_moder(self):
        return self.role_id == app.config['MODERROLE_ID']

    @property
    def is_user(self):
        return self.role_id == app.config['USERROLE_ID']

    @property
    def full_name(self):
        return ' '.join([self.surname, self.name, self.lastname or ''])

    def can(self, action, record=None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False

    def __repr__(self):
        return '<User %r>' % self.login

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    pages = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name

    @property
    def get_genres(self):
        return Genre.query.join(BookGenre).filter(BookGenre.book_id == self.id).all()
        
    @property
    def count_reviews(self):
        return Review.query.filter(Review.book_id == self.id, Review.status_id == 2).count()

    @property
    def get_midscore(self):
        count = Review.query.filter(Review.book_id == self.id, Review.status_id == 2).count()
        reviews = Review.query.filter(Review.book_id == self.id, Review.status_id == 2).all()
        if count == 0:
            return 0
        midscore = 0
        for review in reviews:
            midscore += review.score
        return midscore / count


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class BookGenre(db.Model):
    __tablename__ = 'books_genres'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())
    object_id = db.Column(db.Integer)
    object_type = db.Column(db.String(100))

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)

class ReviewStatus(db.Model):
    __tablename__ = 'rstatuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('rstatuses.id'))
    score = db.Column(db.Integer, nullable=False)
    rtext = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    def __repr__(self):
        return '<Review %r>' % self.id

    @property
    def get_name_user(self):
        return User.query.get(self.user_id).full_name
    
    @property
    def get_book_name(self):
        return Book.query.get(self.book_id).name

    @property
    def get_status_name(self):
        return ReviewStatus.query.get(self.status_id).name
