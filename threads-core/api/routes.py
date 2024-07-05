from .resources.item import (
    ItemResource
)
from .resources.user import UserResource
from .resources.user import Login


def add_routes(api):
    api.add_resource(ItemResource, "/item-resource")
    api.add_resource(UserResource, "/register")
    api.add_resource(Login, "/login")
    

    