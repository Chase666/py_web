from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Genre, Book, BookGenre, Review
from app import db, app
import bleach
import markdown
import math
from auth import check_rights

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/<int:book_id>/new', methods=['GET', 'POST'])
@login_required
def create_review(book_id):
    if request.method == "POST":
        score = request.form.get('score') or 5
        score = int(score)
        rtext = request.form.get('rtext')
        if rtext:
            rtext = bleach.clean(rtext)
        else:
            flash("При добавлении возникла ошибка.", "danger")
            return render_template('reviews/create.html', score=score)

        try:
            new_review = Review(book_id=book_id, user_id=current_user.id, status_id=1, 
                                score=score, rtext=rtext)
            db.session.add(new_review)
            db.session.commit()
            flash("Рецензия успешно добавлена.", "success")
            return redirect(url_for('book.show', book_id = book_id))
        except:
            flash("При добавлении возникла ошибка.", "danger")
            db.session.rollback()
            return render_template('reviews/create.html', score=score)
        
    return render_template('reviews/create.html', score=5)

@bp.route('/show')
@login_required
@check_rights("show_review")
def show_all_review():
    page = request.args.get('page', 1, type=int)
    review_count = Review.query.filter(Review.status_id == app.config['UNWATCHED_REVIEW_STAT_ID']).count()
    page_count = math.ceil(review_count / app.config['REVIEWS_PER_PAGE'])
    all_review = Review.query.filter(Review.status_id == app.config['UNWATCHED_REVIEW_STAT_ID']).limit(app.config['REVIEWS_PER_PAGE']).offset(app.config['REVIEWS_PER_PAGE'] * (page - 1)).all()

    return render_template('reviews/index.html', reviews = all_review,page = page, page_count = page_count)

@bp.route('/<int:review_id>/show')
@login_required
def show_review(review_id):
    review = Review.query.get(review_id)
    review.rtext = markdown.markdown(review.rtext)
    return render_template('reviews/show.html', review = review)



@bp.route('/<int:review_id>/approve', methods=['GET', 'POST'])
@login_required
@check_rights("show_review")
def approve(review_id):
    review = Review.query.get(review_id)
    try:
        review.status_id = 2
        db.session.commit()
        flash("Статус успешно обнавлен.", "success")
    except:
        flash("При изменении статуса возникла ошибка.", "danger")
        db.session.rollback()

    all_review = Review.query.filter(Review.status_id == 1).all()
    # return render_template('reviews/index.html', reviews = all_review)
    return redirect(url_for('review.show_all_review'))

@bp.route('/<int:review_id>/disapprove', methods=['GET', 'POST'])
@login_required
@check_rights("show_review")
def disapprove(review_id):
    review = Review.query.get(review_id)
    try:
        review.status_id = 3
        db.session.commit()
        flash("Статус успешно обнавлен.", "success")
    except:
        flash("При изменении статуса возникла ошибка.", "danger")
        db.session.rollback()

    all_review = Review.query.filter(Review.status_id == 1).all()
    return redirect(url_for('review.show_all_review'))

@bp.route('/user_review')
@login_required
def show_user_review():
    reviews = Review.query.filter(Review.user_id == current_user.id).all()
    for review in reviews:
        review.rtext = markdown.markdown(review.rtext)
    return render_template('reviews/uindex.html', reviews = reviews)