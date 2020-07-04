from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
import datetime
import math
import matplotlib.pyplot as plt
import io

baseW = 504
baseH = 384

def graph(df):
    posIncrease = df['positiveIncrease']
    yticks = [
        posIncrease.min(),
        posIncrease.median(),
        posIncrease.max()
    ]

    reversed = df[::-1]
    plt.style.use('seaborn')
    plt.stackplot(reversed['date'],
                  reversed['positiveIncrease'], color='#d38fc5')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    plt.tick_params(
        axis='y',
        which='both',
        labelleft=False,
        labelright=True
    )
    plt.gcf().set_size_inches(4, 3)

    f = io.BytesIO()
    plt.savefig(f, bbox_inches='tight')
    return f.getvalue()

headerH = math.floor(baseH/8)
subheaderH = math.floor(baseH/10)

def build_image(graph_blob, conf):
    """
    Using the graph data from before, and the data frame we want to build an
    easily digestible image showing key metrics to help assess current status.
    """
    with Image(width=baseW, height=baseH, background='#ffffff') as base:
        with Image(blob=graph_blob) as grph:
            base.composite(grph, math.floor(
                baseW / 7), math.floor(baseH / 5))

        draw_header(base)
        draw_subheader(base, firstDate, lastDate)

        base.format = 'png'
        base.save(filename=f"fig-{conf['name'].replace(' ','_')}.png")


def draw_header(base, conf):

    # Draw a header background.
    with Drawing() as draw:
        draw.fill_color = '#d38fc5'
        draw.rectangle(left=0, top=0, width=baseW, height=math.floor(baseH/8))
        draw(base)

    # Layer header text ontop of background.
    with Drawing() as draw:
        fontSize = 24

        heading = f"COVID-19 in {conf['name']}: New Cases Daily"

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
            '14 days ending in {}'.format(lastDate.strftime('%b %d, %Y')),
            '14 days ending in {}'.format(firstDate.strftime('%b %d, %Y'))
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
