""" Plots based on the ratings a user gives books. """

__author__ = "Eve Sherratt"

# Standard library imports
import os

# External imports
import numpy as np
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt
from fuzzywuzzy import process, fuzz

# Internal arguments
from parse_goodreads_csv import filter_by_month, parse_goodreads_csv
from utils import make_y_axis_out_of_five, format_standard_x_axis, add_title_labels, parse_standard_arguments

def group_publishers_with_similar_names(df):
    """ Helper function to group publishers with similar names,
    to streamline the plot of rating given publisher.
    For example, it should identify 'Publisher Ltd' and 'Publisherltd' as the same publisher.

    Made using tutorial available at:

    https://towardsdatascience.com/fuzzywuzzy-
    find-similar-strings-within-one-column-in-
    a-pandas-data-frame-99f6c2a0c212 """

    # Create a list of all publishers in the dataframe
    unique_publishers = df[df["Publisher"].notnull()]["Publisher"].unique().tolist()

    # For each publisher, check for similar named publishers
    for publisher in unique_publishers:

        y = process.extract(publisher,
                          unique_publishers, scorer=fuzz.token_sort_ratio)
        x = pd.DataFrame(y, columns=["pub","score"])

        similar_names = x[x["score"] > 78]

        if similar_names.shape[0] != 1:
            for name in similar_names["pub"]:

                df = df.replace(to_replace=[name], value=publisher)

                unique_publishers.remove(name)

    return df

def plot_rating_over_time(df, colour, save_plots, year):
    """ Display a user's book ratings over time. """

    # Axis formatting and labels
    ax = plt.axes()
    format_standard_x_axis(ax, year)
    make_y_axis_out_of_five(plt)

    plt.xlabel("Date read")
    plt.ylabel("Rating /5")

    plt.title(f"Your ratings over time {year}")

    # Scatter plot
    plt.scatter(df["Date Read"], df["My Rating"], color=colour)

    # Show book title on hover
    add_title_labels(ax, df)

    # Optionally save plots as png
    if save_plots is True:
        plt.savefig(os.path.join(f"{year}rating", "rating_over_time.png"))

    plt.show()

def compare_personal_to_public_rating(df, colour, save_plots, year):
    """ Plot user book rating against average public rating. """

    my_plot = plt.scatter(df["Average Rating"], df["My Rating"],
                          color=colour)

    plt.title(f"Your rating {year} vs. public rating")

    # Axes formatting
    make_y_axis_out_of_five(plt)
    add_title_labels(my_plot, df)
    plt.xticks([*range(6)])
    plt.xlabel("Average public rating /5")
    plt.ylabel("Your rating /5")
    plt.xlim(0,5.5)
    plt.ylim(0,5.5)

    if save_plots is True:
        plt.savefig(os.path.join("rating", "rating_public_vs_pesonal.png"))

    plt.show()

def plot_rating_given_publish_date(df, colour, save_plots, year):
    """ Display rating in relation to publish date. """

    # Plot title
    plt.title("Rating given year published")

    my_plot = plt.scatter(df["Original Publication Year"], df["My Rating"], color=colour)

    # Formatting
    make_y_axis_out_of_five(plt)
    add_title_labels(my_plot, df)
    plt.xlabel("Original Publication Year")
    plt.ylabel("Rating /5")

    # Save plot as png
    if save_plots is True:
        plt.savefig(os.path.join(f"{year}rating", "rating_publication_year.png"))

    plt.show()

def plot_rating_given_upload_and_read_time_diff(df, colour, save_plots, year):
    """ Display rating given read time, in terms of days to read and page rate. """

    ## Read time in number of days ##

    # Calculate the read time difference
    df["Read Time"] = (df["Date Read"] -  df["Date Added"]) / np.timedelta64(1, 'D')
    read_time_df = df[df["Read Time"] >= 0]
    read_time_df = read_time_df.reset_index(drop=True)

    # Scatter plot
    days_plot = plt.scatter(read_time_df["Read Time"], read_time_df["My Rating"], color=colour)

    # Formatting
    plt.title(f"Number of days between book added and marked as read {year}")
    plt.xlabel("Reading time (days)")
    plt.ylabel("Rating /5")
    make_y_axis_out_of_five(plt)
    add_title_labels(days_plot, read_time_df)

    if save_plots is True:
        plt.savefig(os.path.join(f"{year}rating", "rating_daily_pace.png"))

    plt.show()


    ## Read time by page rate ##

    # Calculate the page rate
    df["Read Time"] = df["Number of Pages"] / ((df["Date Read"] -  df["Date Added"])/ np.timedelta64(1, 'D'))
    read_time_df = df[df["Read Time"] >= 0]
    read_time_df = read_time_df.reset_index(drop=True)

    # Scatter plot
    rate_plot = plt.scatter(read_time_df["Read Time"], read_time_df["My Rating"], color=colour)

    # Formatting
    plt.title("Rating given page reading speed in days")
    plt.xlabel("Pages read per day (rate)")
    plt.ylabel("Rating /5")
    make_y_axis_out_of_five(plt)
    add_title_labels(rate_plot, read_time_df)

    if save_plots is True:
        plt.savefig(os.path.join(f"{year}rating", "rating_page_rate.png"))

    plt.show()

def plot_rating_given_publisher(df, colour, save_plots, year):
    """ Display the average rating given publisher. """

    # Group publishers with similar names using fuzzywuzzy
    df = group_publishers_with_similar_names(df)

    # Group by publisher name
    groupby_publisher = df.groupby(["Publisher"], sort=False).agg({"My Rating": "mean"})

    fig, ax = plt.subplots(figsize=(11,7))

    ax.bar(groupby_publisher.index, groupby_publisher["My Rating"], color = colour)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(rotation=90, size=6)

    plt.title("Average rating given publisher")
    plt.xlabel("Publisher")
    plt.ylabel("Average rating /5")

    if save_plots is True:
        plt.savefig(os.path.join(f"{year}rating", "rating_given_publisher.png"))

    plt.show()

def average_rating_per_month(df, colour, save_plots, year):
    """ Display the average user rating per month, optionally filtered to a specific year. """

    if year != "":
        plt.bar(df.index, df["My Rating"], color=colour, width=0.5)
    else:
        # Set a colour map using the user specified colour
        c_map = colors.LinearSegmentedColormap.from_list("", [(0., colour), (1.0, '#21e5ff')])

        # Create bar chart
        df["My Rating"].plot(kind='bar', colormap=c_map) #, figsize=(11,7))

        # Add legend
        plt.legend(title="Year")
        plt.tight_layout(pad=3)

    make_y_axis_out_of_five(plt)

    plt.xlabel("Month")
    plt.ylabel("Average rating /5")
    plt.title("Monthly average rating")

    if save_plots is True:
        plt.savefig(os.path.join(f"{year}rating", "rating_monthly.png"))

    plt.show()


def main():

    args = parse_standard_arguments()

    if args.year is None:
        args.year = ""

    if args.save_plots is True:
        if not os.path.exists(f"{args.year}rating"):
            os.makedirs(f"{args.year}rating")

    # Load data
    df = parse_goodreads_csv(args.goodreads_csv, args.year)

    # Plots
    plot_rating_over_time(df, args.colour, args.save_plots, args.year)
    compare_personal_to_public_rating(df, args.colour, args.save_plots, args.year)
    plot_rating_given_publish_date(df, args.colour, args.save_plots, args.year)
    plot_rating_given_upload_and_read_time_diff(df, args.colour, args.save_plots, args.year)
    plot_rating_given_publisher(df, args.colour, args.save_plots, args.year)

    # Plots filtered by month
    monthly_df = filter_by_month(df, args.year)
    average_rating_per_month(monthly_df, args.colour, args.save_plots, args.year)


if __name__ == "__main__":
    main()
