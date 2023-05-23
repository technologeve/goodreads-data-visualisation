""" Parses the csv a user can download from their Goodreads account. """

# External imports
import pandas as pd

# Internal imports
from utils import MONTH_ORDER


def parse_goodreads_csv(file, year=None):
    """ Parse user reading data exported from Goodreads as a csv.

    Keyword arguments:
    file:   The filepath to the CSV file exported from a user's Goodreads account.
    year:   Optionally, filter to only parse data from a specified year.

    """

    # Load file
    df = pd.read_csv(file, sep=",", dtype={"My Review": "str"})

    # Format dates to pandas Timestamps
    df["Date Read"] = pd.to_datetime(df["Date Read"], format="%d/%m/%Y")
    df["Date Added"] = pd.to_datetime(df["Date Added"], format="%d/%m/%Y")

    # Create month and year read column
    if year:
        df["Month Read"] = df["Date Read"].dt.strftime("%b")
    else:
        df["Month Read"] = df["Date Read"].dt.strftime("%Y-%b")
    df["Year Read"] = df["Date Read"].dt.year.astype("Int64")


    # Drop any currently reading
    df = df[df["Exclusive Shelf"] != "currently-reading"]

    # Drop unused columns
    df = df.drop(["Owned Copies", "Bookshelves with positions"], axis=1)

    # Filter by year read if provided
    if year:
        df = df[df["Year Read"] == float(year)]
        df = df.reset_index(drop=True)

    # Reverse order, so that date read is ascending
    df = df.sort_values(by="Date Read")

    # Reset indexes
    df = df.reset_index(drop=True)
    return df


def filter_by_month(df, year):

    if year != "":
        # Count number of books read / month
        month_total = df.groupby(["Month Read"], sort=False).agg({"My Rating": "mean",
            "Average Rating": "mean", "Number of Pages":'sum', "Year Published": "mean",
            "Original Publication Year": "mean", "Year Read": "mean"})

        # Data formatting
        df["Number of Pages"] = df["Number of Pages"].astype('Int64')


    else:
        # Group by month and year
        month_total = df.groupby([df["Date Read"].dt.month_name(), df["Year Read"]]).mean().unstack()
        month_total = month_total.reindex(MONTH_ORDER, axis=0)

    return month_total
