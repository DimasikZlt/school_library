from flask_restful import Resource, abort, fields, marshal_with

from library.models.book import Book
from library.models.user import User

author_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'middle_name': fields.String,
    'last_name': fields.String,
}

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.List(fields.Nested(author_fields)),
}

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean(),
    'books': fields.List(fields.Nested(book_fields)),
}


class OrderApi(Resource):
    def get_order_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, error=f"Could not find user with id={user_id}")
        return user

    @marshal_with(user_fields, envelope='order')
    def get(self, user_id):
        return self.get_order_by_id(user_id)


class OrdersApi(Resource):
    @marshal_with(user_fields, envelope='orders')
    def get(self):
        db_fields = (User.last_name, User.first_name)
        users = User.query.join(User.books).order_by(*db_fields, Book.title).all()
        if not users:
            abort(404, error=f"Could not get any orders")
        return users
