from .resources.item import (
    ItemResource
)

def add_routes(api):
    api.add_resource(ItemResource, "/item-resource")