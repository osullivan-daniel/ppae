import json
import pytest
import logging
import subprocess

log = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='config/dev.json')


@pytest.fixture(scope='session')
def guiConfig(request, pytestconfig):
    env = pytestconfig.getoption('env')

    with open(env, 'r') as jsonFile:
        cfg = json.load(jsonFile)

    config = cfg['env']['gui']

    return config