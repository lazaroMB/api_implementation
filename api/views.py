from flask import request, jsonify
from dependency_injector.wiring import inject, Provide

from .services import DataService
from .containers import Container


@inject
def index(data_service: DataService = Provide[Container.data_service]):
    args = request.args
    category = args.get('category')
    result = {}
    if category is None:
        result = data_service.get_categories_statistics()
    else:
        result = data_service.get_category_statistics(category)
    return jsonify(result)
