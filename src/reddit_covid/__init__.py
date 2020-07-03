__version__ = "0.1.0"

from . import fetch
from . import present


def main():
    df = fetch.fetch()

    present.build_image(present.graph(df), df)
