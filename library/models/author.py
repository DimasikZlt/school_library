from library import db


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), nullable=False)
    books = db.relationship('Book', backref='author', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f"<Author {self.last_name} {self.first_name[0]}. {self.middle_name[0]}.>"

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}. {self.middle_name[0]}."


db.Index('authors_name_index', Author.last_name, Author.first_name, Author.middle_name)
