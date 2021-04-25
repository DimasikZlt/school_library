from flask import jsonify
from flask_restful import Resource, abort, fields, marshal_with, reqparse, marshal
from sqlalchemy.exc import IntegrityError

from library import db
from library.models.user import User

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean()
}


class UserApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True, location='json',
                                   help='User first name is required')
        self.reqparse.add_argument('last_name', type=str, required=True, location='json',
                                   help='User last name is required')
        self.reqparse.add_argument('email', type=str, required=True, location='json',
                                   help="User email is required")
        self.reqparse.add_argument('password_hash', type=str, location='json',
                                   help='User password')
        self.reqparse.add_argument('is_admin', type=bool, required=True, location='json',
                                   help='User admin is required')
        super().__init__()

    def get_user_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, error=f"Could not find user with id={user_id}")
        return user

    @marshal_with(user_fields, envelope='user')
    def get(self, user_id):
        return self.get_user_by_id(user_id)

    def put(self, user_id):
        user = self.get_user_by_id(user_id)
        args = self.reqparse.parse_args()
        user.first_name = args['first_name']
        user.last_name = args['last_name']
        user.email = args['email']
        user.is_admin = args['is_admin']
        if args['password_hash']:
            user.password_hash = user.set_password(args['is_admin'])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(400, error=f"User with email {args['email']} already exists")
        return marshal(user, user_fields, envelope='user')

    def delete(self, user_id):
        user = self.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': 'OK'})


class UsersApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True, location='json',
                                   help='User first name is required')
        self.reqparse.add_argument('last_name', type=str, required=True, location='json',
                                   help='User last name is required')
        self.reqparse.add_argument('email', type=str, required=True, location='json',
                                   help="User email is required")
        self.reqparse.add_argument('password_hash', type=str, required=True, location='json',
                                   help='User password is required')
        self.reqparse.add_argument('is_admin', type=bool, required=True, location='json',
                                   help='User admin is required')
        super().__init__()

    @marshal_with(user_fields, envelope='users')
    def get(self):
        users = User.query.all()
        if not users:
            abort(404, error=f"Could not get any users")
        return users

    def post(self):
        args = self.reqparse.parse_args()
        new_user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            is_admin=args['is_admin']
        )
        new_user.set_password(args['password_hash'])
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(400, error=f"User with email {args['email']} already exists")
        return marshal(new_user, user_fields, envelope='user')
