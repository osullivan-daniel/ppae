import logging
import pytest
import json

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


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "./.testVideoRecordings"
    }
