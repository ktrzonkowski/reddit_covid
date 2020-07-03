__version__ = "0.1.0"

from . import fetch
from . import present
from . import constants


def main():

    for state in constants.stateConfig.keys():
        df = fetch.fetch(state)
        present.build_image(present.graph(df), constants.stateConfig[state])
