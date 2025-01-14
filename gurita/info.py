'''
Module      : describe 
Description : Display summary information about the columns in the current data frame 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import pandas as pd
from gurita.command_base import CommandBase
import gurita.utils as utils
import gurita.constants as const 

class Describe(CommandBase, name="describe"):
    description = "Show summary information about the input data set."
    category = "summary information"
    
    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--columns', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns')


    def run(self, df):
        options = self.options
        rows, cols = df.shape
        pd.set_option('display.max_columns', None)
        if options.columns:
            utils.validate_columns_error(df, options.columns)
            print(df[options.columns].describe(include='all'))
        else:
            print(df.describe(include='all'))
        return df


class Pretty(CommandBase, name="pretty"):
    description = "Pretty print a fragment of the data set."
    category = "summary information"
    
    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--columns', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns')
        self.optional.add_argument(
            '--maxrows', metavar='NUM', type=int, required=False, default=const.DEFAULT_PRETTY_MAX_ROWS,
            help=f'Maximum number of rows to pretty print. Default: %(default)s.')
        self.optional.add_argument(
            '--maxcols', metavar='NUM', type=int, required=False, default=const.DEFAULT_PRETTY_MAX_COLS,
            help=f'Maximum number of columns to pretty print. Default: %(default)s.')


    def run(self, df):
        options = self.options
        selected_df = df
        if options.columns:
            utils.validate_columns_error(df, options.columns)
        print(selected_df.to_string(columns=options.columns, header=True, max_rows=options.maxrows, max_cols=options.maxcols, show_dimensions=False, index=False))
        nrows, ncols = df.shape
        print(f"\n[{nrows} rows x {ncols} columns]")
        return df


class Unique(CommandBase, name="unique"):
    description = "Print the unique values from a column."
    category = "summary information"
    
    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--column', metavar='COLUMN', type=str, required=False,
            help=f'Select unique items from this column')
        self.optional.add_argument(
            '--sort', action='store_true',
            default=False, required=False,
            help=f'Sort the items in ascending order')


    def run(self, df):
        options = self.options
        utils.check_df_has_columns(df, [options.column])
        this_unique = df[options.column].unique()
        if options.sort:
            this_unique.sort()
        print("\n".join(this_unique))
