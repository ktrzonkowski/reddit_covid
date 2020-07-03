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
    df.plot(
        x='date', y='positiveIncrease', linewidth=2.0, color='blue', ax=ax)
    plt.legend('', frameon=False)
    f = io.BytesIO()
    plt.savefig(f)
    return f.getvalue()

baseW = 504
baseH = 384

headerH = math.floor(baseH/8)
subheaderH = math.floor(baseH/10)

def build_image(graph_blob, df):
    """
    Using the graph data from before, and the data frame we want to build an
    easily digestible image showing key metrics to help assess current status.
    """
    firstDate = df['date'][0]
    lastDate = df['date'][28]

    with Image(width=baseW, height=baseH, background='#ffffff') as base:
        with Image(blob=graph_blob) as grph:
            base.composite(grph, math.floor(
                baseW / 8), math.floor(baseH / 2))

        draw_header(base)
        draw_subheader(base, firstDate, lastDate)

        base.format = 'png'
        base.save(filename='fig.png')


def draw_header(base):

    # Draw a header background.
    with Drawing() as draw:
        draw.fill_color = '#32B332'
        draw.rectangle(left=0, top=0, width=baseW, height=headerH)
        draw(base)

    # Layer header text ontop of background.
    with Drawing() as draw:
        fontSize = 20

        heading = "COVID-19 in North Carolina: Daily Case Increases"

        (verticalAlign, horizontalAlign) = calculate_alignment(base, draw, headerH, baseW, heading)

        draw.font_size = fontSize
        draw.fill_color = '#E4FFE3'
        draw.text(10, verticalAlign, heading)
        draw(base)

def draw_subheader(base, firstDate, lastDate):

    # Draw subheader bottom border
    with Drawing() as draw:
        draw.fill_color = '#3C3C3C'
        draw.rectangle(left=0, top=(headerH + subheaderH), width=baseW, height=5)
        draw(base)

    # Apply subheaders
    with Drawing() as draw:
        fontSize = 14

        draw.font_size = fontSize
        draw.fill_color = '#5254C7'

        subheadings = [
            f'14 days ending in {firstDate}',
            f'14 days ending in {lastDate}'
        ]

        for i in range(2):
            (verticalAlign, horizontalAlign) = calculate_alignment(base, draw, subheaderH, math.floor(baseW/2), subheadings[i])

            # Print a subheading on the left or right side
            # left  = (baseW / 2) * 0
            # right = (baseW / 2) * 1
            draw.text(math.floor(baseW/2*i) + horizontalAlign, headerH + verticalAlign, subheadings[i])
            draw(base)

def calculate_alignment(base, draw, height, width, text):
    """
    Calculate the vertical and horizontal aligment values
    necessary to center given text in a specific area.
    """
    metrics = draw.get_font_metrics(base, text)

    # Vertical alignment calculation
    # half height + half text height
    verticalAlign = math.floor( (height/2) + (metrics.text_height/2) )

    # Horizontal alignment calculation
    # half width - half text width
    horizontalAlign = math.floor( (width/2) - (metrics.text_width/2) )

    return ( verticalAlign, horizontalAlign )
