"""
conftest.py according to pytest docs:
https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re#conftest-py-plugins
"""
import pytest

from testcontainers.core.container import DockerContainer

from energytt_platform.bus import get_default_broker


@pytest.fixture(scope='function')
def kafka_container():
    """
    TODO
    """
    kafka_docker = DockerContainer('landoop/fast-data-dev:latest')
    kafka_docker.env.update({'ADV_HOST': 'localhost'})
    kafka_docker.ports.update({
        2181: 2181,
        3030: 3030,
        8081: 8081,
        8082: 8082,
        8083: 8083,
        9581: 9581,
        9582: 9582,
        9583: 9583,
        9584: 9584,
        9585: 9585,
        9092: 9092,
    })

    with kafka_docker as container:
        import time
        time.sleep(30)
        yield container


@pytest.fixture(scope='function')
def broker(kafka_container):
    """
    TODO
    """
    host = kafka_container.get_container_host_ip()
    port = kafka_container.get_exposed_port(9092)
    server = f'{host}:{port}'
    # x = kafka_container.get_container_host_ip()
    # j = 2

    yield get_default_broker(
        group='test-group',
        servers=[server],
    )
