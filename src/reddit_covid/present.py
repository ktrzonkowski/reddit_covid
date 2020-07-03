from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
import math
import matplotlib.pyplot as plt
import io


def graph(df):
    """
    Builds the graph of two 2 week periods of positive COVID-19 cases.
    """
    fig = plt.figure(frameon=False, figsize=(4., .5), dpi=100)
    ax = fig.add_axes((0., 0., .95, 1))
    ax.set_axis_off()
    df[:28].plot(
        x='date', y='positiveIncrease', linewidth=2.0, color='blue', ax=ax)
    plt.legend('', frameon=False)
    f = io.BytesIO()
    plt.savefig(f)
    return f.getvalue()


baseW = 504
baseH = 384


def build_image(graph_blob, df):
    """
    Using the graph data from before, and the data frame we want to build an
    easily digestible image showing key metrics to help assess current status.
    """
    firstDate = df['date'][0]
    lastDate = df['date'][28]

    with Drawing() as draw:
        with Image(width=baseW, height=baseH) as base:
            with Image(blob=graph_blob) as grph:
                base.composite(grph, math.floor(
                    baseW / 8), math.floor(baseH / 2))

            draw.font_size = 40
            draw.text(0,
                      40, 'Hello, world!')
            draw.text(0, 80, f'{firstDate}')
            draw.text(0, 120, f'{lastDate}')
            draw(base)
            base.format = 'jpeg'
            base.save(filename='fig.jpg')
