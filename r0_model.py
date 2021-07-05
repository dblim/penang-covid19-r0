"""
Author: David Benjamin Lim
Website: http://dblim.github.io
License: MIT
"""
import argparse
import datetime
import numpy as np 
import os
import pandas as pd 
import sys

from params import *

def calculate_r0(args):
    # Get arguments:
    input_dir = args.input_dir
    input_file = args.input_file
    output_dir = args.output_dir
    output_file = args.output_file
    input_start = args.start
    input_end = args.end

    # Load data
    abs_path = os.path.join(input_dir, input_file)
    df = pd.read_csv(abs_path)

    # Length of entire dataframe
    n = len(df)

    # Get dates. Convert everything to datetime object
    dates = pd.to_datetime(df['date'])
    output = pd.DataFrame(0, index=dates, columns=SUBREGIONS)

    # Define start and end dates. Default is the whole dataframe
    start = dates.iloc[0]
    end = dates.iloc[-1]

    if input_start:
        start = pd.to_datetime(input_start)
    if input_end:
        end = pd.to_datetime(input_end)

    # Select portion of dataframe corresponding to start and end dates
    mask = (dates >= start) & (dates <= end)
    df = df.loc[mask]

    # This is the length of the truncated dataframe
    n = len(df)

    if n < R0_WINDOW:
        print("The number of days between start and end dates is less than R0_WINDOW."
              + "\n" + "Please select valid start and end dates.")
        sys.exit()

    ans = []
    for t in range(n- R0_WINDOW + 1):

        day = [df['date'].iloc[t + R0_WINDOW-1]]

        for s in SUBREGIONS:
            x = [i for i in range(R0_WINDOW)]

            # Take log of data befor doing OLS
            y = np.log(df[s].iloc[t : t + R0_WINDOW])

            X = np.vstack([x, np.ones(len(x))]).T

            b, ln_a = np.linalg.lstsq(X, y, rcond=None)[0]

            r_0 = np.exp(b*SERIAL_INT)

            # print(s + ': {:.3f}'.format(r_0))
            day.append(r_0)

        ans.append(day) 
    output = pd.DataFrame(ans, columns = ['date'] + SUBREGIONS).round(3)
    
    # Save output of r0_values to csv file
    location = os.path.join(output_dir, output_file)
    output.to_csv(location)

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to compute R_0 values.')
    parser.add_argument('input_dir', type=str, help='The input directory.')
    parser.add_argument('input_file', type=str, help='The name of your data file.')
    parser.add_argument('output_dir', type=str, help='The output directory.')
    parser.add_argument('output_file',type=str, help='The name of your output file.')
    parser.add_argument('--start', type=str, help='The start date to compute R_0'
                        + ' values for. The default is R0_WINDOW days from' +
                        ' the start of the file.')
    parser.add_argument('--end', type=str, help='The end date to compute R_0' 
                        + ' values for. The default is the end of the file.')

    args = parser.parse_args()

    output = calculate_r0(args)

