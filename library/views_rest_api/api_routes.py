from library.views_rest_api.api_orders_view import OrdersApi, OrderApi
from library.views_rest_api.api_user_view import UserApi, UsersApi


def register_api_routes(api):
    api.add_resource(UserApi, "/api/users/<int:user_id>")
    api.add_resource(UsersApi, "/api/users")
    api.add_resource(OrderApi, "/api/orders/<int:user_id>")
    api.add_resource(OrdersApi, "/api/orders")
