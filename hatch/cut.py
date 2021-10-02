'''
Module      : cut 
Description : Select (retain) a subset of columns from the dataset by name, and drop all the others
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import pandas as pd
from hatch.command_base import CommandBase
import hatch.utils as utils
from hatch.constants import PROGRAM_NAME

class Cut(CommandBase, name="cut"):
    description = "Select a subset of columns by name." 
    category = "transformation"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-c', '--columns', metavar='NAME', nargs="+", type=str, required=False,
        help=f'Select only these named columns')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        if options.columns is not None:
            columns = options.columns
            valid_columns, invalid_columns = utils.validate_columns(df, columns)
            if valid_columns:
                df = df[valid_columns]
            else:
                print(f"{PROGRAM_NAME} {self.name} WARNING: no valid columns were specified")
                # return None as the result, we should stop here 
                df = None 
            if invalid_columns:
                print(f"{PROGRAM_NAME} {self.name} WARNING: the following requested columns are not in the data, and could not be selected:")
                print("\n".join(invalid_columns))
        return df
