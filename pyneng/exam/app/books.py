from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Genre, Book, BookGenre, Review
from app import db
import bleach
import markdown
from auth import check_rights

bp = Blueprint('book', __name__, url_prefix='/book')

BOOK_PARAMS = ['name', 'description', 'publisher', 'year', 'author', 'pages']

# Получение всех данных из формы
def get_book_params():
    res = {}
    for params in BOOK_PARAMS:
        res[params] = request.form.get(params)
        if params == 'description' and res['description']:
            res['description'] = bleach.clean(res['description'])
        if params == 'year' and res['year'].isdigit() and res['year']:
            res['year'] = int(res['year'])
        if params == 'pages' and res['pages'].isdigit() and res['pages']:
            res['pages'] = int(res['pages'])
    return res

# Для просмотра
@bp.route('/<int:book_id>/show')
@check_rights("show")
def show(book_id):
    # Загрузка книги
    book = Book.query.get(book_id)
    book.description = markdown.markdown(book.description)

    # Рецензии
    book_review = Review.query.filter(Review.book_id == book_id, Review.status_id == 2).all()
    for review in book_review:
        review.rtext = markdown.markdown(review.rtext)
    # book_review = Review.query.filter(Review.book_id == book_id).all()
    book_review_user = Review.query.filter(Review.book_id == book_id, Review.user_id == current_user.id).all()

    if book_review_user:
        create_review = False
    else:
        create_review = True


    return render_template('books/show.html', book = book, reviews = book_review, create_review = create_review)

# Создание жанров
def create_genre(book_id):
    genre_id_list =  request.form.getlist('genres')
    for genre_id in genre_id_list:
        try:
            book_genre = BookGenre(book_id = book_id, genre_id = genre_id)
            db.session.add(book_genre)
            db.session.commit()
        except:
            db.session.rollback()

# Для создания новой книги
@bp.route('/new', methods=['GET', 'POST'])
@login_required
@check_rights("new")
def new():
    # Получение всех жанров
    genres = Genre.query.all()
    if request.method == "POST":
        # Получение параметров для книги
        book_params = get_book_params()
        create_genres = request.form.getlist('genres')
        create_genres_id = [int(x) for x in create_genres]

        # Проверка на cуществование жанров
        if not create_genres_id:
            flash("При добавлении возникла ошибка.", "danger")
            return render_template('books/new.html', genres=genres, book=book_params)

        # Добавление книги
        try:
            book = Book(**book_params)
            db.session.add(book)
            db.session.commit()
            flash("Книга успешно добавлена.", "success")
            create_genre(book.id)
            return redirect(url_for('index'))
        except:
            flash("При добавлении возникла ошибка.", "danger")
            db.session.rollback()
            book_params['genre_list'] = create_genres_id
            return render_template('books/new.html', genres=genres, book=book_params)

    return render_template('books/new.html', genres=genres, book={})

# Удаление всех жанров по определенной книге
def delete_all_genre(book_id):
        genres_book = BookGenre.query.filter(BookGenre.book_id == book_id).all()
        for genres_book_one in genres_book:
            db.session.delete(genres_book_one)
            db.session.commit()


# Для изменения книги
@bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights("edit")
def edit(book_id):
    # Загрузка книги
    book = Book.query.get(book_id)
    book_params = {}
    book_params['name'] = book.name
    book_params['description'] = book.description
    book_params['year'] = book.year
    book_params['publisher'] = book.publisher
    book_params['author'] = book.author
    book_params['pages'] = book.pages

    book_genres_id = []
    book_genres = book.get_genres
    for book_genres_one in book_genres:
        book_genres_id.append(book_genres_one.id)
    book_params['genre_list'] = book_genres_id
    
    # Получение всех жанров
    genres = Genre.query.all()
    

    if request.method == "POST":
        # Получение новых параметров для книги
        new_book_params = get_book_params()
        create_genres = request.form.getlist('genres')
        create_genres_id = [int(x) for x in create_genres]

        # Проверка на cуществование жанров
        if not create_genres_id:
            flash("При добавлении возникла ошибка.", "danger")
            return render_template('books/new.html', genres=genres, book=book_params)

        # Изменение книги
        try:
            book.name = new_book_params['name']
            book.author = new_book_params['author']
            book.description = new_book_params['description']
            book.year = new_book_params['year']
            book.publisher = new_book_params['publisher']
            book.pages = new_book_params['pages']

            db.session.commit()
            delete_all_genre(book.id)
            create_genre(book.id)
            flash("Книга успешно изменена.", "success")
            return redirect(url_for('index'))
        except:
            flash("При изменении возникла ошибка.", "danger")
            db.session.rollback()
            return redirect(url_for('index'))

    return render_template('books/edit.html', genres=genres, book=book_params)

# Для удаления книги
@bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
@check_rights("delete")
def delete(book_id):
    try:
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash("Книга удалена изменена.", "success")
    except:
        db.session.rollback()
        flash("При удалении возникла ошибка.", "danger")
    return redirect(url_for('index'))

