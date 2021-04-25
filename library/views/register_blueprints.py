from library.views import (
    about_view,
    users_view,
    authors_view,
    books_view,
    orders_view,
    users_auth_view
)


def register_blueprints(app):
    app.register_blueprint(about_view.blueprint)
    app.register_blueprint(users_view.blueprint)
    app.register_blueprint(authors_view.blueprint)
    app.register_blueprint(books_view.blueprint)
    app.register_blueprint(orders_view.blueprint)
    app.register_blueprint(users_auth_view.blueprint)
