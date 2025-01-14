'''
Module      : plot 
Description : Plotting functions 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import sys
import argparse
import logging
import seaborn as sns
import matplotlib.pyplot as plt
from gurita.command_base import CommandBase
import gurita.render_plot as render_plot
import gurita.io_arguments as io_args 
from gurita.plot_arguments import make_plot_arguments, x_argument, y_argument, hue, row, col, order, hue_order, orient, logx, logy, xlim, ylim, dotsize, dotsizerange, dotalpha, dotlinewidth, dotlinecolour, dotstyle, colwrap, dodge, vlines, hlines, strip, nooutliers, estimator
import gurita.constants as const
import gurita.utils as utils


class PairPlot(CommandBase, name="pair"):
    description = "Pair plot of numerical features."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments,
                   make_plot_arguments(const.DEFAULT_PAIR_PLOT_WIDTH,
                                                 const.DEFAULT_PAIR_PLOT_HEIGHT)]
        super().__init__(parents)
        self.optional.add_argument(
            '-c', '--columns', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns')
        self.optional.add_argument(
            '--kind',  type=str, required=False,
            choices=const.ALLOWED_PAIRPLOT_KINDS, default=const.DEFAULT_PAIR_PLOT_KIND,
            help=f'Kind of plot to use. Allowed values: %(choices)s. Default: %(default)s.')
        self.optional.add_argument(
            '--corner', action='store_true', required=False,
            default=False,
            help=f'Only plot the lower triangle of comparisons')
        hue(self)
        hue_order(self)


    def run(self, df):
        options = self.options
        _width_inches, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        kwargs = {}
        graph = sns.pairplot(data=df, height=height_inches, aspect=aspect,
                vars=options.columns, kind=options.kind, hue=options.hue, hue_order=options.hueorder,
                corner=options.corner, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df

class BarPlot(CommandBase, name="bar"):
    description = "Bar plot of categorical feature."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        estimator(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        group = self.optional.add_mutually_exclusive_group()
        group.add_argument('--std', action='store_true', default=False, required=False, help=f'Show standard deviation of numerical feature as error bar')
        group.add_argument('--ci', metavar='NUM', type=float, required=False, nargs='?', const=const.DEFAULT_CI, help=f'Show confidence interval as error bar to estimate uncertainty of point estimate')


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        estimator_fun = utils.make_estimator(options.estimator)
        error_indicator = options.ci
        if options.std:
            error_indicator = 'sd' 
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, estimator=estimator_fun,
                ci=error_indicator,
                col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class BoxPlot(CommandBase, name="box"):
    description = "Plot distrbution of numerical column using box-and-whiskers."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        strip(self)
        nooutliers(self)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                showfliers=not(options.nooutliers),
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.strip:
            graph.map_dataframe(sns.stripplot, data=df, x=options.xaxis, y=options.yaxis, alpha=0.8, color="black", order=options.order)
        render_plot.render_plot(options, graph, self.name)
        return df


class BoxenPlot(CommandBase, name="boxen"):
    description = "Plot distrbution of numerical column using boxes for quantiles."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        strip(self)
        nooutliers(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                showfliers=not(options.nooutliers),
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.strip:
            graph.map_dataframe(sns.stripplot, data=df, x=options.xaxis, y=options.yaxis, alpha=0.8, color="black")
        render_plot.render_plot(options, graph, self.name)
        return df


class Clustermap(CommandBase, name="clustermap"):
    description = "Clustered heatmap of two categorical columns." 
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        self.required.add_argument(
            '-v', '--val', metavar='COLUMN', required=True, type=str,
            help=f'Interpret this feature (column of data) as the values of the heatmap')
        self.optional.add_argument(
            '--cmap',  metavar='COLOR_MAP_NAME', type=str, required=False,
            help=f'Use this color map, will use Seaborn default if not specified')
        self.optional.add_argument(
            '--log', action='store_true', required=False,
            help=f'Use a log scale on the numerical data')
        self.optional.add_argument(
            '--dendroratio', metavar='NUM', type=float, default=const.DEFAULT_DENDRO_RATIO,
            required=False, help=f'Ratio of the figure size devoted to the dendrogram. Default: %(default)s.')
        self.optional.add_argument('--rowclust', dest='rowclust', action='store_true',
            required=False, help='Cluster by rows (default).')
        self.optional.add_argument('--no-rowclust', dest='rowclust', action='store_false',
            required=False, help='Do not cluster by rows')
        self.optional.set_defaults(rowclust=True)
        self.optional.add_argument('--colclust', dest='colclust', action='store_true',
            required=False, help='Cluster by columns (default).')
        self.optional.add_argument('--no-colclust', dest='colclust', action='store_false',
            required=False, help='Do not cluster by columns')
        # clustermap does not allow both zscore and standard_scale to be specified at the same time
        cluster_normalise_group = self.optional.add_mutually_exclusive_group()
        cluster_normalise_group.add_argument('--zscore', required=False, choices=['y', 'x'],
            help='Normalise either across rows (y) or down columns (x) using z-score. Allowed values: %(choices)s.')
        cluster_normalise_group.add_argument('--stdscale', required=False, choices=['y', 'x'],
            help='Normalise either across rows (y) or down columns (x) by subtracting the minimum and dividing by the maximum. Allowed values: %(choices)s.')
        self.optional.add_argument('--method', required=False,
            choices=const.ALLOWED_CLUSTERMAP_METHODS, default=const.DEFAULT_CLUSTERMAP_METHOD,
            help='Linkage method to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
        self.optional.add_argument('--metric', required=False,
            choices=const.ALLOWED_CLUSTERMAP_METRICS, default=const.DEFAULT_CLUSTERMAP_METRIC,
            help='Distance metric to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
        self.optional.add_argument(
            '--annot', action='store_true', required=False,
            help=f'Display the data value in each cell in the heatmap')
        # See https://docs.python.org/3/library/string.html#formatspec for options on formatting
        self.optional.add_argument(
            '--fmt', type=str, required=False, 
            help=f'String formatting to be used for displaying cell values using Python format specification, used in conjunction with --annot.')
        self.optional.add_argument(
            '--vmin', type=float, metavar='NUM', required=False,
            help=f'Minimum anchor value for the colormap, if unset this will be inferred from the dataset')
        self.optional.add_argument(
            '--vmax', type=float, metavar='NUM', required=False,
            help=f'Maximum anchor value for the colormap, if unset this will be inferred from the dataset')
        self.optional.add_argument(
            '--robust', action='store_true',
            help=f'If --vmin or --vmax absent, use robust quantiles to set colormap range instead of the extreme data values')
        self.optional.set_defaults(colclust=True)


    def run(self, df):
        options = self.options
        if options.xaxis not in df.columns:
            utils.exit_with_error(f"{options.xaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.yaxis not in df.columns:
            utils.exit_with_error(f"{options.yaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.val not in df.columns:
            utils.exit_with_error(f"{options.val} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        self.x = options.xaxis
        self.y = options.yaxis
        self.val = options.val
        pivot_data = df.pivot(index=self.y, columns=self.x, values=self.val)
        width_inches, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        figsize = (width_inches, height_inches)
        kwargs = {}
        if options.zscore == 'y':
            kwargs['z_score'] = 0
        elif options.zscore == 'x':
            kwargs['z_score'] = 1
        if options.stdscale == 'y':
            kwargs['standard_scale'] = 0
        elif options.stdscale == 'x':
            kwargs['standard_scale'] = 1
        xticklabels = True
        if options.nxtl:
            xticklabels = False
        yticklabels = True
        if options.nytl:
            yticklabels = False
        # the following arguments control heatmap aspects of the clustermap
        kwargs['annot'] = self.options.annot
        kwargs['fmt'] = self.options.fmt
        kwargs['robust'] = self.options.robust
        kwargs['vmin'] = self.options.vmin
        kwargs['vmax'] = self.options.vmax
        # same time, even if only one is None.
        graph = sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                      dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                      col_cluster=options.colclust, yticklabels=yticklabels, xticklabels=xticklabels,
                      method=options.method, metric=options.metric, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class Heatmap(CommandBase, name="heatmap"):
    description = "Heatmap of two categorical columns." 
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        self.required.add_argument(
            '-x', '--xaxis', metavar='COLUMN', required=True, type=str,
            help=f'Feature to plot along the X axis.')
        self.required.add_argument(
            '-y', '--yaxis', metavar='COLUMN', required=True, type=str,
            help=f'Feature to plot along the Y axis.')
        self.required.add_argument(
            '-v', '--val', metavar='COLUMN', required=True, type=str,
            help=f'Interpret this feature (column of data) as the values of the heatmap')
        self.optional.add_argument(
            '--cmap',  metavar='COLOR_MAP_NAME', type=str, required=False,
            help=f'Use this color map, will use Seaborn default if not specified')
        self.optional.add_argument(
            '--annot', type=str, required=False, nargs='?', metavar='FORMAT',
            const=const.DEFAULT_HEATMAP_STRING_FORMAT,
            help=f'Display the data value in each cell in the heatmap. Optional FORMAT argument uses Python format specifcation (default: %(const)s)')
        # See https://docs.python.org/3/library/string.html#formatspec for options on formatting
        #parser.add_argument(
        #    '--fmt', type=str, required=False, 
        #    help=f'String formatting to be used for displaying cell values using Python format specification, used in conjunction with --annot. Uses Python format specifications.')
        self.optional.add_argument(
            '--vmin', type=float, metavar='NUM', required=False,
            help=f'Minimum anchor value for the colormap, if unset this will be inferred from the dataset')
        self.optional.add_argument(
            '--vmax', type=float, metavar='NUM', required=False,
            help=f'Maximum anchor value for the colormap, if unset this will be inferred from the dataset')
        self.optional.add_argument(
            '--robust', action='store_true', required=False,
            help=f'If --vmin or --vmax absent, use robust quantiles to set colormap range instead of the extreme data values')
        #parser.add_argument(
        #    '--log', action='store_true',
        #    help=f'Use a log scale on the numerical data')
        x_order_group = self.optional.add_mutually_exclusive_group()
        x_order_group.add_argument(
            '--sortx',  type=str, required=False, nargs='?',
            choices=const.ALLOWED_SORT_ORDER, default=const.DEFAULT_SORT_ORDER,
            help=f'Sort the X axis by label. Allowed values: %(choices)s. a=ascending, d=descending. Default: %(default)s. Categorical features will be sorted alphabetically. Numerical features will be sorted numerically.')
        x_order_group.add_argument(
            '--orderx', metavar='VALUE', type=str, required=False, nargs='+',
            help=f'Order the X axis according to a given list of values, left to right. Unlisted values will appear in arbitrary order.')
        y_order_group = self.optional.add_mutually_exclusive_group()
        y_order_group.add_argument(
            '--sorty', type=str, required=False, nargs='?',
            choices=const.ALLOWED_SORT_ORDER, default=const.DEFAULT_SORT_ORDER,
            help=f'Sort the Y axis by label. Allowed values: %(choices)s. a=ascending, d=descending. Default: %(default)s. Categorical features will be sorted alphabetically. Numerical features will be sorted numerically.')
        y_order_group.add_argument(
            '--ordery', metavar='VALUE', type=str, required=False, nargs='+',
            help=f'Order the Y axis according to a given list of values, top to bottom. Unlisted values will appear in arbitrary order.')


    def run(self, df):
        options = self.options
        if options.xaxis not in df.columns:
            utils.exit_with_error(f"{options.xaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.yaxis not in df.columns:
            utils.exit_with_error(f"{options.yaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.val not in df.columns:
            utils.exit_with_error(f"{options.val} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        self.x = options.xaxis
        self.y = options.yaxis
        self.val = options.val
        kwargs = {}
        if options.annot is not None:
            kwargs['fmt'] = options.annot
            kwargs['annot'] = True
        pivot_data = df.pivot(index=self.y, columns=self.x, values=self.val)
        if self.options.sortx is not None:
            ascending = True if self.options.sortx == 'a' else False
            pivot_data.sort_index(axis=1, ascending=ascending, inplace=True)
        if self.options.sorty is not None:
            ascending = True if self.options.sorty == 'a' else False
            pivot_data.sort_index(axis=0, ascending=ascending, inplace=True)
        if self.options.orderx is not None:
            # orderx must not have duplicates
            if len(self.options.orderx) != len(set(self.options.orderx)):
                utils.exit_with_error("X axis labels for ordering contains duplicates", const.EXIT_COMMAND_LINE_ERROR)
            # orderx must be a subset of the column labels
            column_label_strings = pivot_data.columns.map(str)
            if not set(self.options.orderx).issubset(set(column_label_strings)):
                utils.exit_with_error("X axis labels for ordering are not a subset of column labels", const.EXIT_COMMAND_LINE_ERROR)
            order_map = { item: pos for (pos, item) in enumerate(self.options.orderx) }
            max_index = len(self.options.orderx)
            pivot_data.sort_index(axis=1, inplace=True, key=lambda index: index.map(lambda label: order_map.get(str(label), max_index)))
        if self.options.ordery is not None:
            # ordery must not have duplicates
            if len(self.options.ordery) != len(set(self.options.ordery)):
                utils.exit_with_error("Y axis labels for ordering contains duplicates", const.EXIT_COMMAND_LINE_ERROR)
            # ordery must be a subset of the row labels
            row_label_strings = pivot_data.index.map(str)
            if not set(self.options.ordery).issubset(set(row_label_strings)):
                utils.exit_with_error("Y axis labels for ordering are not a subset of row labels", const.EXIT_COMMAND_LINE_ERROR)
            order_map = { item: pos for (pos, item) in enumerate(self.options.ordery) }
            max_index = len(self.options.ordery)
            pivot_data.sort_index(axis=0, inplace=True, key=lambda index: index.map(lambda label: order_map.get(str(label), max_index)))
        width_inches, height_inches, _aspect = utils.plot_dimensions_inches(options.width, options.height) 
        fig, ax = plt.subplots(figsize=(width_inches, height_inches))
        graph = sns.heatmap(data=pivot_data, cmap=self.options.cmap, robust=self.options.robust,
                    vmin=self.options.vmin, vmax=self.options.vmax, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class HistogramPlot(CommandBase, name="hist"):
    description = "Histogram of numerical or categorical feature."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        vlines(self)
        hlines(self)
        self.optional.add_argument(
            '--multiple', required=False, choices=const.ALLOWED_HIST_MULTIPLES,
            help=f"How to display overlapping subsets of data in a histogram. Allowed values: %(choices)s.")
        self.optional.add_argument(
            '--bins', metavar='NUM', required=False, type=int, default=const.DEFAULT_HISTOGRAM_BINS,
            help=f'Number of histogram bins. Default: %(default)s.')
        self.optional.add_argument(
            '--binwidth', metavar='NUM', required=False, type=float,
            help=f'Width of histogram bins, overrides "--bins".')
        self.optional.add_argument(
            '--cumulative', action='store_true', required=False,
            help=f'Generate cumulative histogram')
        self.optional.add_argument(
           '--kde', action='store_true', required=False,
            help=f'Plot a kernel density estimate for the histogram and show as a line')
        self.optional.add_argument(
           '--nofill', action='store_true', required=False,
            help=f'Use unfilled histogram bars instead of solid coloured bars')
        self.optional.add_argument(
           '--element', choices=const.ALLOWED_HISTOGRAM_ELEMENTS, default=const.DEFAULT_HISTOGRAM_ELEMENT,
           required=False, help=f'Style of histogram bars. Allowed values: %(choices)s. Default: %(default)s')
        self.optional.add_argument(
           '--stat', choices=const.ALLOWED_HISTOGRAM_STATS, default=const.DEFAULT_HISTOGRAM_STAT,
           required=False,
           help=f'Statistic to use for each bin. Allowed values: %(choices)s. Default: %(default)s')
        self.optional.add_argument(
           '--indnorm', action='store_true', required=False,  
           help=f'For normalised statistics (e.g. percent), normalise each histogram in the plot independently, otherwise normalise over the full dataset')


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        if options.bins:
            kwargs['bins'] = options.bins
        if options.binwidth:
            kwargs['binwidth'] = options.binwidth
        if options.multiple:
            kwargs['multiple'] = options.multiple
        if options.kde:
            kwargs['kde'] = options.kde
        log_axes = [False, False]
        if options.logx:
            log_axes[0] = True
            del options.logx
        if options.logy:
            log_axes[1] = True 
            del options.logy
        kwargs['log_scale'] = tuple(log_axes) 
        kwargs['element'] = options.element
        kwargs['fill'] = not(options.nofill)
        if options.xaxis is not None and options.yaxis is not None:
            # element and fill are only defined for univariate data
            kwargs.pop('element', None)
            kwargs.pop('fill', None)
        graph = sns.displot(kind='hist', data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                cumulative=options.cumulative,
                hue_order=options.hueorder,
                stat=options.stat,
                common_norm=not(options.indnorm),
                facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.vlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.vlines:
                    ax.axvline(pos)
        if options.hlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.hlines:
                    ax.axhline(pos)
        render_plot.render_plot(options, graph, self.name)
        return df


class LinePlot(CommandBase, name="line"):
    description = "Line plot of numerical feature."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        vlines(self)
        hlines(self)
    

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.relplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.vlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.vlines:
                    ax.axvline(pos)
        if options.hlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.hlines:
                    ax.axhline(pos)
        render_plot.render_plot(options, graph, self.name)
        return df


class PointPlot(CommandBase, name="point"):
    description = "Point plot of numerical feature."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class ScatterPlot(CommandBase, name="scatter"):
    description = "Scatter plot comparing two features as dot plot"
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        dotsize(self)
        dotalpha(self)
        dotlinewidth(self)
        dotstyle(self)
        dotsizerange(self)
        dotlinecolour(self)
        vlines(self)
        hlines(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        facet_kws = { 'legend_out': True }
        kwargs = {}
        if options.dotlinewidth is not None:
            kwargs['linewidth'] = options.dotlinewidth
        if options.dotlinecolour is not None:
            kwargs['edgecolor'] = options.dotlinecolour 
        sizes = None
        if options.dotsizerange is not None:
            sizes=tuple(options.dotsizerange)
        graph = sns.relplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                style=options.dotstyle, sizes=sizes, size=options.dotsize, alpha=options.dotalpha,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.vlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.vlines:
                    ax.axvline(pos)
        if options.hlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.hlines:
                    ax.axhline(pos)
        render_plot.render_plot(options, graph, self.name)
        return df


class LMPlot(CommandBase, name="lmplot"):
    description = "Regression plot"
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        hue_order(self)
        colwrap(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        facet_kws = { 'legend_out': True }
        kwargs = {}
        scatter_kws = {}
        graph = sns.lmplot(data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                hue_order=options.hueorder, scatter_kws=scatter_kws, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class StripPlot(CommandBase, name="strip"):
    description = "Plot distrbution of numerical column using dotted strip."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        dodge(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                dodge = options.dodge,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class SwarmPlot(CommandBase, name="swarm"):
    description = "Plot distrbution of numerical column using dot swarm."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        dodge(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder, dodge=options.dodge,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class ViolinPlot(CommandBase, name="violin"):
    description = "Plot distrbution of numerical column using violin."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)
        strip(self)


    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.strip:
            graph.map_dataframe(sns.stripplot, data=df, x=options.xaxis, y=options.yaxis, alpha=0.8, color="black", order=options.order)
        render_plot.render_plot(options, graph, self.name) 
        return df


class CountPlot(CommandBase, name="count"):
    description = "Plot count of categorical columns using bars."
    category = "plotting"

    def __init__(self):
        parents = [io_args.io_arguments, make_plot_arguments()]
        super().__init__(parents)
        x_argument(self)
        y_argument(self)
        hue(self)
        row(self)
        col(self)
        order(self)
        hue_order(self)
        orient(self)
        logx(self)
        logy(self)
        xlim(self)
        ylim(self)
        colwrap(self)


    def run(self, df):
        options = self.options
        if options.xaxis is not None and options.yaxis is not None:
            utils.exit_with_error("You cannot use both -x (--xaxis) and -y (--yaxis) at the same time in a count plot", const.EXIT_COMMAND_LINE_ERROR)
        if options.xaxis is None and options.yaxis is None:
            utils.exit_with_error("A count plot requires either -x (--xaxis) OR -y (--yaxis) to be specified", const.EXIT_COMMAND_LINE_ERROR)
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder, 
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df
