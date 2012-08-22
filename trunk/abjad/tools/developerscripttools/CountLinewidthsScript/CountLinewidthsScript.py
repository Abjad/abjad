from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
import argparse
import importlib
import os


class CountLinewidthsScript(DirectoryScript):
    '''Tabulate the linewidths of modules in a path:

    ::

        bash$ ajv count linewidths -h
        usage: count-linewidths [-h] [--version] [-l N] [-o w|m] [-C | -D] [-a | -d]
                                [-gt N | -lt N | -eq N]
                                path

        Count maximum line-width of all modules in PATH.

        positional arguments:
          path                  directory tree to be recursed over

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit
          -l N, --limit N       limit output to last N items
          -o w|m, --order-by w|m
                                order by line width [w] or module name [m]
          -C, --code            count linewidths of all code in module
          -D, --docstrings      count linewidths of all docstrings in module
          -a, --ascending       sort results ascending
          -d, --descending      sort results descending
          -gt N, --greater-than N
                                line widths greater than N
          -lt N, --less-than N  line widths less than N
          -eq N, --equal-to N   line widths equal to N
         
    Return `CountLinewidthsScript` instance.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'linewidths'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'count'

    @property
    def short_description(self):
        return 'Count maximum line-width of all modules in PATH.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):

        #print args

        modules = {}

        if args.mode == 'docstrings':
            print 'DOCS:\tMODULE:'
            for obj in documentationtools.FunctionCrawler(args.path)():
                docstring = obj.__doc__
                if not docstring:
                    modules[obj.__module__] = 0
                else:
                    lines = docstring.split('\n')
                    modules[obj.__module__] = max([len(line) for line in lines])
            for obj in documentationtools.ClassCrawler(args.path)():
                docstring = obj.__doc__
                width = 0
                if docstring:
                    lines = docstring.split('\n')
                    width = max([len(line) for line in lines])
                for attr_name in dir(obj):
                    attr = getattr(obj, attr_name)
                    attr_docstring = getattr(attr, '__doc__', None)
                    if attr_docstring:
                        lines = attr_docstring.split('\n')
                        attr_width = max([len(line) for line in lines])
                        if width < attr_width:
                            width = attr_width
                modules[obj.__module__] = width

        elif args.mode == 'code':
            print 'CODE:\tMODULE:'
            for obj in documentationtools.FunctionCrawler(args.path)():
                module_path = obj.__module__
                module_obj = importlib.import_module(module_path)
                module_filename = module_obj.__file__
                if module_filename.endswith('.pyc'):
                    module_filename = module_filename[:-1]
                with open(module_filename, 'r') as f:
                    lines = f.read().split('\n')
                    modules[obj.__module__] = max([len(line) for line in lines])
            for obj in documentationtools.ClassCrawler(args.path)():
                module_path = obj.__module__
                module_obj = importlib.import_module(module_path)
                module_filename = module_obj.__file__
                if module_filename.endswith('.pyc'):
                    module_filename = module_filename[:-1]
                with open(module_filename, 'r') as f:
                    lines = f.read().split('\n')
                    modules[obj.__module__] = max([len(line) for line in lines])

        if args.order_by == 'm':
            order_by = lambda x: (x[0], x[1])
        else:
            order_by = lambda x: (x[1], x[0])

        if args.sort == 'descending':
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

    def setup_argument_parser(self, parser):

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

        mode_group = parser.add_mutually_exclusive_group()

        mode_group.add_argument('-C', '--code',
            action='store_const',
            const='code',
            dest='mode',
            help='count linewidths of all code in module',
            )

        mode_group.add_argument('-D', '--docstrings',
            action='store_const',
            const='docstrings',
            dest='mode',
            help='count linewidths of all docstrings in module',
            )

        sort_group = parser.add_mutually_exclusive_group()

        sort_group.add_argument('-a', '--ascending',
            action='store_const',
            const='ascending',
            dest='sort',
            help='sort results ascending',
            )

        sort_group.add_argument('-d', '--descending',
            action='store_const',
            const='descending',
            dest='sort',
            help='sort results descending',
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

        parser.set_defaults(mode='docstrings', order_by='w', sort='ascending')
