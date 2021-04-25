from library import db, login_manager, bcrypt
from flask_login import UserMixin


orders = db.Table(
    'orders',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('books_id', db.Integer, db.ForeignKey('books.id'))
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password_hash = db.Column(db.String(512), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    is_admin = db.Column(db.Boolean)

    books = db.relationship(
        'Book',
        secondary='orders',
        backref=db.backref('users', lazy='select'),
        lazy='select'
    )

    def __repr__(self):
        return f"<User {self.last_name} {self.first_name}>"

    def __str__(self):
        return f"{self.last_name} {self.first_name} "

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def is_password_ok(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


db.Index('users_name_index', User.last_name, User.first_name, User.email)
