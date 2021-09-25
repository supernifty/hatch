'''
Module      : count_plot 
Description : Create a count plot from the data 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import seaborn as sns
import hatch.render_plot as render_plot
import hatch.io_arguments as io_args 
import hatch.plot_arguments as plot_args 
import hatch.constants as const
import hatch.utils as utils
import argparse

class CountPlot:
    def __init__(self):
        self.options = None

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind='count', data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.facet_plot(options, graph, 'count')
        return df

    def parse_args(self, args):
        parser = argparse.ArgumentParser(parents=[
               io_args.io_arguments, plot_args.plot_arguments,
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
           add_help=False)
        # XXX Catch exceptions here
        self.options = parser.parse_args(args)
        if self.options.xaxis is not None and self.options.yaxis is not None:
            utils.exit_with_error("You cannot use both -x (--xaxis) and -y (--yaxis) at the same time in a count plot", const.EXIT_COMMAND_LINE_ERROR)
        if self.options.xaxis is None and self.options.yaxis is None:
            utils.exit_with_error("A count plot requires either -x (--xaxis) OR -y (--yaxis) to be specified", const.EXIT_COMMAND_LINE_ERROR)