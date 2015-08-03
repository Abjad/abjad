# -*- encoding: utf-8 -*-
import importlib
from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class CountLinewidthsScript(DirectoryScript):
    r'''Counts linewidths of modules in a path.

    ..  shell::

        ajv count linewidths --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'linewidths'``.
        '''
        return 'linewidths'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns ``'count'``.
        '''
        return 'count'

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Count maximum line-width of all modules in PATH.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''

        #print args

        modules = {}

        if args.mode == 'docstrings':
            print('DOCS:\tMODULE:')
            for obj in documentationtools.yield_all_functions(args.path):
                docstring = obj.__doc__
                if not docstring:
                    modules[obj.__module__] = 0
                else:
                    lines = docstring.split('\n')
                    modules[obj.__module__] = \
                        max([len(line) for line in lines])
            for obj in documentationtools.yield_all_classes(args.path):
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
            print('CODE:\tMODULE:')
            for obj in documentationtools.yield_all_functions(args.path):
                module_path = obj.__module__
                module_obj = importlib.import_module(module_path)
                module_file_name = module_obj.__file__
                if module_file_name.endswith('.pyc'):
                    module_file_name = module_file_name[:-1]
                with open(module_file_name, 'r') as f:
                    lines = f.read().split('\n')
                    modules[obj.__module__] = \
                        max([len(line) for line in lines])
            for obj in documentationtools.yield_all_classes(args.path):
                module_path = obj.__module__
                module_obj = importlib.import_module(module_path)
                module_file_name = module_obj.__file__
                if module_file_name.endswith('.pyc'):
                    module_file_name = module_file_name[:-1]
                with open(module_file_name, 'r') as f:
                    lines = f.read().split('\n')
                    modules[obj.__module__] = \
                        max([len(line) for line in lines])

        if args.order_by == 'm':
            order_by = lambda x: (x[0], x[1])
        else:
            order_by = lambda x: (x[1], x[0])

        if args.sort == 'descending':
            modules = sorted(list(modules.items()), key=order_by, reverse=True)
        else:
            modules = sorted(list(modules.items()), key=order_by)

        if args.greater_than is not None and 0 < args.greater_than:
            modules = [pair for pair in modules if args.greater_than < pair[1]]
        elif args.less_than is not None and 0 < args.less_than:
            modules = [pair for pair in modules if pair[1] < args.less_than]
        elif args.equal_to is not None and 0 <= args.equal_to:
            modules = [pair for pair in modules if pair[1] == args.equal_to]

        if args.limit is not None and 0 < args.limit:
            modules = modules[-args.limit:]

        for pair in modules:
            print('{}\t{}'.format(pair[1], pair[0]))

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
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