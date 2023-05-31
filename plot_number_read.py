""" Plots based on the number of books a user has read. """

# Standard library imports
import os

# External imports
from matplotlib import colors
import matplotlib.pyplot as plt

# Internal arguments
from utils import rotate_and_shrink_x_axis, parse_standard_arguments
from parse_goodreads_csv import filter_by_month, parse_goodreads_csv

def plot_number_of_books_over_time(df, colour, save_plots, year):
    """ Display the number of books a user has read over time. """

    # Plot title
    plt.title(f"Number of books read per month {year}")

    # Count number of books read / month
    month_total = df.groupby(["Month Read"], sort=False).size()

    plt.bar(month_total.index, month_total, width=0.5, color=colour)

    # Axis labels
    plt.xlabel("Month")
    plt.ylabel("Number of books read")
    rotate_and_shrink_x_axis(plt, month_total.index)

    # Save plot as png
    if save_plots is True:
        plt.savefig(os.path.join(f"{year}number_read", "number_over_time.png"))

    plt.show()

def pages_read_per_month(monthly_df, colour, save_plots, year):
    """ Display the number of pages a user has read over time. """

    if year == "":
        # Set a colour map using the user specified colour
        c_map = colors.LinearSegmentedColormap.from_list("", [(0., colour), (1.0, '#21e5ff')])

        # Create bar chart
        monthly_df["Number of Pages"].plot(kind='bar', colormap=c_map)

        # Add legend
        plt.legend(title="Year")
        plt.tight_layout(pad=3)

    else:
        plt.bar(monthly_df.index, monthly_df["Number of Pages"], color=colour, width=0.5)


    # Title, axes labels
    plt.xlabel("Month")
    plt.ylabel("Total monthly number of pages read")
    plt.title(f"Number of pages read per month {year}")

    # Save plot as png
    if save_plots is True:
        plt.savefig(os.path.join(f"{year}number_read", "monthly_pages.png"))

    plt.show()


def main():

    args = parse_standard_arguments()

    if args.year is None:
        args.year = ""

    if args.save_plots is True:
        if not os.path.exists(f"{args.year}number_read"):
            os.makedirs(f"{args.year}number_read")


    # Load data
    df = parse_goodreads_csv(args.goodreads_csv, args.year)

    # Plots
    plot_number_of_books_over_time(df, args.colour, args.save_plots, args.year)

    # Plots filtered by month
    monthly_df = filter_by_month(df, args.year)
    pages_read_per_month(monthly_df, args.colour, args.save_plots, args.year)


if __name__ == "__main__":
    main()
