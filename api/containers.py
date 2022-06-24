from dependency_injector import containers, providers
from . import services
import json


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=['.views'])

    data_service = providers.Factory(
            services.DataService, data=json.load(open('data.json')))
