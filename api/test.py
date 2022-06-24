from unittest import mock
import json

import pytest
from flask import url_for

from .application import create_app
from .services import DataService


def json_of_response(response):
    return json.loads(response.data.decode('utf8'))


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()


def test_get_category_statistics_endpoint(client, app):
    right_data = {'category': 'Food', 'price': 1, 'percentage_discount': 0}
    wrong_data = {}
    service_data_mock = mock.Mock(spec=DataService)
    service_data_mock.get_category_statistics.return_value = right_data
    service_data_mock.get_categories_statistics.return_value = wrong_data
    with app.container.data_service.override(service_data_mock):
        response = client.get(url_for("index", category='Food'))

    assert response.status_code == 200
    assert json_of_response(response) == right_data


def test_get_categories_statistics_endpoint(client, app):
    right_data = {'Food': 1, 'Electronics': 1}
    wrong_data = {}
    service_data_mock = mock.Mock(spec=DataService)
    service_data_mock.get_category_statistics.return_value = wrong_data
    service_data_mock.get_categories_statistics.return_value = right_data
    with app.container.data_service.override(service_data_mock):
        response = client.get(url_for("index"))

    assert response.status_code == 200
    assert json_of_response(response) == right_data


def test_categories_statistics(client, app):
    right_data = [
            {'category': 'Food', 'price': 1, 'percentage_discount': 0},
            {'category': 'Electronic', 'price': 1, 'percentage_discount': 0.1},
            ]
    a = DataService(data=right_data)
    assert a.get_categories_statistics() == {'Food': 1, 'Electronic': 0.999}


def test_category_statistics(client, app):
    right_data = [
            {'category': 'Food', 'price': 1, 'percentage_discount': 0},
            {'category': 'Electronic', 'price': 1, 'percentage_discount': 0.1},
            ]
    a = DataService(data=right_data)
    assert a.get_category_statistics('Food') == {'Food': 1}
    assert a.get_category_statistics('Electronic') == {'Electronic': 0.999}
