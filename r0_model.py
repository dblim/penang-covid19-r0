"""
Author: David Benjamin Lim
Website: http://dblim.github.io
License: MIT
"""
import argparse
import datetime
import numpy as np
import pandas as pd
import sys
import params

DATE_FMT = '%d-%m-%Y'

def check_dates(start, data_start, input_start, end, data_end, input_end,
                R0_WINDOW):
    """Checks if user start and end dates (for R0 calculation) are valid given
    the data start and end dates and R0_WINDOW value"""

    # note that start is <= input_start
    if input_start and (input_start > data_end):
        err_msg = ("\nSelected dates are not covered by data.\nYour start "
                    "date is %s, End date of data is %s.")
        err_data = tuple(map(lambda x: x.strftime(DATE_FMT) if x else None,\
                                           (input_start, data_end)))
        raise ValueError(err_msg % err_data)

    if (start < data_start)  or\
            (end < data_start or end > data_end):
        err_msg = ("\nSelected dates are not covered by data.\n Your start "
            "and end dates are     %s to %s, \n which requires data running "
            "from %s to %s. \n Start and end dates of data are "
            " %s to %s. \n Selected R0_WINDOW is %d days.")
        err_data = list(map(lambda x: x.strftime(DATE_FMT) if x else None,\
                                   (input_start, input_end, start, end,\
                                    data_start, data_end)))
        err_data.append(R0_WINDOW)
        err_data = tuple(err_data)
        raise ValueError(err_msg % err_data)
    if (end - data_start).days < R0_WINDOW -1:
        err_msg = ("\nEnd date must be at least R0_WINDOW-1 days earlier than"
                   " data start date.\nYour end date is %s. Data start date "
                   "is %s. Earliest possible end date is %s. Selected "
                   "R0_WINDOW is %d days.")
        err_data = list(map(lambda x: x.strftime(DATE_FMT) if x else None,\
                                   (input_end, data_start,
                                    data_start + datetime.timedelta(days=R0_WINDOW-1))))
        err_data.append(R0_WINDOW)
        err_data = tuple(err_data)
        raise ValueError(err_msg % err_data)


# This check is not needed - we just need enough data before the user's start
# date -- Daniel 13.07
#    # Length of calculation period
#    n = (end - start).days
#    if  n < window_length:
#        err_str = """The number of days (%d) between start and end dates is \
#            less than R0_WINDOW (%d).\n Please select valid start and end \
#            dates"""
#        err_params = (n, window_length)
#        raise ValueError(err_str % err_params)

def fit_r0(df, subregion, t, R0_WINDOW, SERIAL_INT):
    """
    Fit and return r0 value for a particular day:
        df: truncated per 100K data frame
        subregion: name of subregion to calculate for
        t: index of start date
    """
    x = [i for i in range(R0_WINDOW)]

    # Take log of data before doing OLS
    y = np.log(df[subregion].iloc[t:t + R0_WINDOW])

    X = np.vstack([x, np.ones(len(x))]).T

    # If numpy version is < 1.14.0, a TypeError is raised for rcond
    try:
        lstsq_output = np.linalg.lstsq(X, y, rcond=None)
    except TypeError:
        lstsq_output = np.linalg.lstsq(X, y, rcond=-1)

    b, ln_a = lstsq_output[0]
    r_0 = np.exp(b*SERIAL_INT)

    return r_0, b, ln_a



def calculate_r0(args):
    # Get arguments:
    input_file = args.input_file
    output_file = args.output_file
    input_start = pd.to_datetime(args.start)
    input_end = pd.to_datetime(args.end)
    if args.window:
        R0_WINDOW = args.window
    else:
        R0_WINDOW = params.R0_WINDOW
    SERIAL_INT = params.SERIAL_INT
    SUBREGIONS = params.SUBREGIONS
    # Load data
    df = pd.read_csv(input_file)

    # Length of entire dataframe
    n = len(df)

    # Get date, subregion names. Convert everything to datetime object
    dates = pd.to_datetime(df['date'])
    # first column is date
    subregions = list(df.columns[1:])


    # Get start and end dates of per100K data
    data_start = dates.iloc[0]
    data_end = dates.iloc[-1]

    # define start and end dates for calculation. Default is start and end
    # dates of per100K data.
    # If user specifies a start date (for R0 values) we need to start the data
    # R0_window days earlier than this.
    start = input_start - datetime.timedelta(days=R0_WINDOW-1) if input_start\
        else data_start
    # first calculated date will be R0_window days after the first date in our
    # data
    #start_R0_date = start + datetime.timedelta(days=R0_WINDOW)
    end = input_end if input_end else data_end

    # Check dates
    check_dates(start, data_start, input_start, end, data_end, input_end,
                R0_WINDOW)
    # Select portion of dataframe corresponding to start and end dates
    mask = (dates >= start) & (dates <= end)
    df = df.loc[mask]
    n = len(df)

    # list to store output
    output_list = []

    for t in range(n - R0_WINDOW + 1):
        day = df['date'].iloc[t + R0_WINDOW-1]
        new_row = [day]

        for s in subregions:
            r_0 = fit_r0(df, s, t, R0_WINDOW, SERIAL_INT)[0]
            new_row.append(r_0)
        output_list.append(new_row)
    #create output DF and make the date column the index
    output = pd.DataFrame(output_list, columns=['date'] + subregions)
    output.set_index('date')

    # Save output of r0_values to csv file
    output = output.round(3)
    output.to_csv(output_file)

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to compute R_0\
                                     values.')
    parser.add_argument('input_file', type=str, help='Path to data file.')
    parser.add_argument('output_file', type=str, help='Path to output file.')
    parser.add_argument('--start', type=str,
                        help=("The start date (format dd-mm-yyyy) to compute "
                              "R_0 values for. The default is R0_WINDOW days "
                              "from the start of the file. Note that the start"
                              "date must be at least R0_WINDOW-1 days later "
                              "than the start of the input file."))
    parser.add_argument('--end', type=str,
                        help=("The end date (format dd-mm-yyyy) to compute R_0"
                              "values for. The default is the end of the file."))
    parser.add_argument('--window', type=int,
                        help=("Time window to fit R0 over. Default is 14 days"))
    parser.add_argument('--diag', type=bool, default=False,
                        help=("Diagnostic flag. If True, both outputs from the"
                              "least squares fit will be output."))

    args = parser.parse_args()

    # parse and validate dates
    if args.start:
        try:
            args.start = datetime.datetime.strptime(args.start, DATE_FMT)
        except ValueError:
            raise ValueError('Incorrect start date format, should be dd-mm-yyy')
    if args.end:
        try:
           args.end = datetime.datetime.strptime(args.end, DATE_FMT)
        except ValueError:
            raise ValueError('Incorrect end date format, should be dd-mm-yyy')
    if args.start and args.end:
        if args.start >= args.end:
            raise ValueError('End date must be later than start date.')
    output = calculate_r0(args)
