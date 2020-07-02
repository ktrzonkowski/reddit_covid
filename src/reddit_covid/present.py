from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
import math


def build_image(graph_blob, df):
    """
    Using the graph data from before, and the data frame we want to build an
    easily digestible image showing key metrics to help assess current status.
    """
    firstDate = df['date'][0]
    lastDate = df['date'][28]

    with Drawing() as draw:
        with Image(blob=graph_blob) as img:
            draw.font_size = 40
            draw.text(0,
                      40, 'Hello, world!')
            draw.text(0, 80, f'{firstDate}')
            draw.text(0, 120, f'{lastDate}')
            draw(img)
            img.format = 'jpeg'
            img.save(filename='fig.jpg')
