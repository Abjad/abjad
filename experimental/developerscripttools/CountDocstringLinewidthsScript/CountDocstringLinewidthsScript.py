#! /usr/bin/env python

from abjad.tools import documentationtools
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import argparse
import os


class CountDocstringLinewidthsScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def long_description(self):
        return None

    @property
    def short_description(self):
        return 'Count maximum line-width of docstrings of all modules in PATH.'

    ### PRIVATE METHODS ###

    def _is_valid_path(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
        return False

    def _process_args(self, args):

        modules = {}

        for obj in documentationtools.FunctionCrawler(args.path)():
            docstring = obj.__doc__
            if not docstring:
                modules[obj.__module__] = 0
            else:
                lines = docstring.split('\n')
                modules[obj.__module__] = max([len(line) for line in lines])

        for obj in documentationtools.ClassCrawler(args.path)():
            docstring = obj.__doc__
            if not docstring:
                modules[obj.__module__] = 0
            else:
                lines = docstring.split('\n')
                modules[obj.__module__] = max([len(line) for line in lines])

        if args.order_by == 'm':
            order_by = lambda x: (x[0], x[1])
        else:
            order_by = lambda x: (x[1], x[0])

        if args.descending:
            modules = sorted(modules.items(), key=order_by, reverse=True)
        else:
            modules = sorted(modules.items(), key=order_by)

        if args.greater_than is not None and 0 < args.greater_than:
            modules = [pair for pair in modules if args.greater_than < pair[1]]
        elif args.less_than is not None and 0 < args.less_than:
            modules = [pair for pair in modules if pair[1] < args.less_than]
        elif args.equal_to is not None and 0 <= args.equal_to:
            modules = [pair for pair in modules if pair[1] == args.equal_to]

        if args.limit is not None and 0 < args.limit:
            modules = modules[-args.limit:]

        for pair in modules:
            print '{}\t{}'.format(pair[1], pair[0])

    def _setup_argument_parser(self, parser):

        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

        parser.add_argument('-l', '--limit',
            help='limit output to last N items',
            metavar='N',
            type=int,
            )

        parser.add_argument('-o', '--order-by',
            choices='wm',
            help='order by line width [w] or module name [m]',
            metavar='w|m',
            type=str,
            )

        sort_group = parser.add_mutually_exclusive_group()

        sort_group.add_argument('-a', '--ascending',
            action='store_true',
            default=True,
            help='sort by ascending line widths',
            )

        sort_group.add_argument('-d', '--descending',
            action='store_true',
            help='sort by descending line widths',
            )

        thresh_group = parser.add_mutually_exclusive_group()

        thresh_group.add_argument('-gt', '--greater-than',
            help='line widths greater than N',
            metavar='N',
            type=int,
            )

        thresh_group.add_argument('-lt', '--less-than',
            help='line widths less than N',
            metavar='N',
            type=int,
            )

        thresh_group.add_argument('-eq', '--equal-to',
            help='line widths equal to N',
            metavar='N',
            type=int,
            )

    def _validate_path(self, path):
        error = argparse.ArgumentTypeError('{!r} is not a valid directory.'.format(path))
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return path


if __name__ == '__main__':
    script_name = os.path.basename(__file__).rstrip('.py')
    eval(script_name)()()
