from flask import Flask, render_template, abort, send_from_directory, request
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import math

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager
from books import bp as book_bp
from review import bp as review_bp

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)


init_login_manager(app)

from models import Book, Image

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    book_count = Book.query.count()
    page_count = math.ceil(book_count / app.config['BOOKS_PER_PAGE'])
    books = Book.query.order_by(Book.year.desc()).limit(app.config['BOOKS_PER_PAGE']).offset(app.config['BOOKS_PER_PAGE'] * (page - 1)).all()
    return render_template(
        'index.html',
        books=books, page=page, page_count=page_count
    )

@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Image, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)
