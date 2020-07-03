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
    fig = plt.figure(frameon=True, figsize=(1.5, .5), dpi=200)
    ax = fig.add_axes((0., 0., .95, 1))
    ax.set_axis_off()
    df[::-1].plot.bar(None, ['positiveIncrease'],
                      stacked=True, ax=ax, rot=0, color=['b', 'r'])
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
    with Image(width=baseW, height=baseH, background='#ffffff') as base:
        with Image(blob=graph_blob) as grph:
            base.composite(grph, math.floor(
                baseW / 5), math.floor(baseH / 2))

        draw_header(base)
        base.format = 'png'
        base.save(filename='fig.png')


def draw_header(base):

    # Draw a header background.
    with Drawing() as draw:
        draw.fill_color = '#7FFF00'
        draw.rectangle(left=0, top=0, width=baseW, height=math.floor(baseH/8))
        draw(base)

    # Layer header text ontop of background.
    with Drawing() as draw:
        draw.font_size = 16
        draw.text(0, 40, 'COVID-19 in North Carolina: New Cases Daily')
        draw(base)
