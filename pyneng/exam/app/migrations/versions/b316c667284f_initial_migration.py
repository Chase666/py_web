"""Initial migration

Revision ID: b316c667284f
Revises: 
Create Date: 2023-06-27 23:04:45.340702

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b316c667284f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['categories.id'], name=op.f('fk_categories_parent_id_categories')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories'))
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genres')),
    sa.UniqueConstraint('name', name=op.f('uq_genres_name'))
    )
    op.create_table('images',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('file_name', sa.String(length=100), nullable=False),
    sa.Column('mime_type', sa.String(length=100), nullable=False),
    sa.Column('md5_hash', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('object_id', sa.Integer(), nullable=True),
    sa.Column('object_type', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_images')),
    sa.UniqueConstraint('md5_hash', name=op.f('uq_images_md5_hash'))
    )
    op.create_table('books_genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_books_genres_book_id_books')),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], name=op.f('fk_books_genres_genre_id_genres')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_books_genres'))
    )
    op.drop_table('reviews')
    op.drop_table('covers')
    op.drop_table('roles')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('lastname',
               existing_type=mysql.VARCHAR(length=88),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=88),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('surname',
               existing_type=mysql.VARCHAR(length=88),
               type_=sa.String(length=100),
               nullable=True)
        batch_op.alter_column('login',
               existing_type=mysql.VARCHAR(length=88),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('role_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.alter_column('phash',
               existing_type=mysql.VARCHAR(length=512),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_users_login'), ['login'])
        batch_op.drop_constraint('users_ibfk_1', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_foreign_key('users_ibfk_1', 'roles', ['role_id'], ['id'])
        batch_op.drop_constraint(batch_op.f('uq_users_login'), type_='unique')
        batch_op.alter_column('phash',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=512),
               existing_nullable=False)
        batch_op.alter_column('role_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.alter_column('login',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=88),
               existing_nullable=False)
        batch_op.alter_column('surname',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=88),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=88),
               existing_nullable=False)
        batch_op.alter_column('lastname',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=88),
               existing_nullable=False)

    op.create_table('roles',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=88), nullable=False),
    sa.Column('description', mysql.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('covers',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('filename', mysql.VARCHAR(length=88), nullable=False),
    sa.Column('mime', mysql.VARCHAR(length=222), nullable=False),
    sa.Column('md5hash', mysql.VARCHAR(length=222), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('reviews',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('book_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('rating', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('rtext', mysql.TEXT(), nullable=False),
    sa.Column('rdate', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='reviews_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='reviews_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('books_genres')
    op.drop_table('images')
    op.drop_table('genres')
    op.drop_table('categories')
    # ### end Alembic commands ###