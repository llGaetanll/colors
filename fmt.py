import numpy as np
from enum import Enum

"""
This file contains various helpers for outputing colors to the terminal
"""

# constant colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def _fg(text, color):
    """
    Sets the foreground color of `text` to `color` which is an `(r, g, b)` tuple
    or array
    """
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m"


def _bg(text, color):
    """
    Sets the background color of `text` to `color` which is an `(r, g, b)` tuple
    or array
    """
    return f"\033[48;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m"


def rgb(color):
    """
    Display the color as RGB
    """

    color_str = ", ".join(
        list(map(lambda channel: f"  {channel}"[-3:], color)))

    return f"RGB({color_str})"


def hexa(color):
    """
    Display the color as HEX
    """

    return "#" + "".join(list(map(lambda channel: f"0{hex(channel)[2:]}"[-2:], color)))


ColorMode = Enum('ColorMode', ['RGB', 'HEX'])


def _color(txt, color):
    """
    Colors some text in the terminal.

    Args:
    - `txt`: An arbitrary string
    - `colors`: An `(r, g, b)` tuple
    """

    brightness = sum(color) / (255 * 3)
    fg_color = BLACK if brightness > 0.3 else WHITE

    return _bg(_fg(txt, fg_color), color)


def to_str(color, color_mode):
    """
    Formats a color to the terminal.

    Args:
    - `color`: An `(r, g, b)` tuple of a given color
    - `color_mode`: Either `RGB` or `HEX`. Represents the in which to display a color
    """

    return rgb(color) if color_mode == ColorMode.RGB else hexa(color)


table = {
    'hex': ['a', 'b', 'c'],
    'rgb': ['a', 'b', 'c'],
}


# find the max width of a single row
def row_width(row):
    header, lst = row

    len_colors = [len(color["str"]) for color in lst]

    return max(len(header), *len_colors)


def table(table):

    # convert color strs
    table = {
        header: [
            {
                "str": to_str(color["color"], color["fmt"]),
                "color": color["color"]
            }
            for color in lst
        ]
        for header, lst in table.items()
    }

    # compute column widths
    widths = list(map(row_width, table.items()))

    rows = []
    for (row, col_width) in zip(table.items(), widths):
        header, lst = row

        # cells are padded with at most `col_width` spaces
        pad = " " * col_width

        # headers are left-aligned
        header_str = f"{header}{pad}"[:col_width]

        # colors are right aligned
        lst_strs = [
            _color(
                f"{pad}{color['str']}"[-col_width:],
                color["color"]
            )
            for color in lst
        ]

        # add new row
        row = [header_str, *lst_strs]
        rows.append(row)

    rows = np.array(rows)
    cols = rows.T

    table = "\n".join(list(map(lambda row_cells: " ".join(row_cells), cols)))

    print(table)
