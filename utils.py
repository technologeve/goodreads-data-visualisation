""" Helper functions. """

# Standard library imports
import argparse

# External imports
import mplcursors
from matplotlib import dates

## Default values ##
DEFAULT_PLOT_COLOUR = "#4c56be"
MONTH_ORDER = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


## Useful functions ##
def add_title_labels(plot, df):
    mplcursors.cursor(plot, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(df["Title"][sel.index]))

def format_standard_x_axis(ax, year):
    if year != "":
        ax.xaxis.set_major_formatter(dates.DateFormatter("%b"))

def make_y_axis_out_of_five(plt):
    plt.yticks([*range(6)])

def rotate_and_shrink_x_axis(plt, x_axis):
    if x_axis.size > 12:
        plt.xticks(rotation=-90, size=6)

def parse_standard_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--goodreads_csv", help="Filepath \
        to the CSV exported from your goodreads account.")
    parser.add_argument("-c", "--colour", help="Colour desired for \
        plots, optional, HEX", default=DEFAULT_PLOT_COLOUR)
    parser.add_argument("-y", "--year", help="Optional filter to \
        restrict plots to books read in a certain year, string in \
        format YYYY", default=None)
    parser.add_argument("-s", "--save_plots", help="Flag which saves\
                         the plots as pngs", action="store_true")

    args = parser.parse_args()

    return args