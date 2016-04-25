# -*- coding: utf-8 -*-
from __future__ import print_function
import inspect
import os
import types
from abjad.tools import stringtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class StatsScript(DirectoryScript):
    r'''Builds statistics about a codebase.

    ..  shell::

        ajv stats  --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'stats'``.
        '''
        return 'stats'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns none.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Build statistics about Python modules in PATH.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PRIVATE METHODS ###

    def _iterate_module(self, module):
        results = []
        for name in dir(module):
            obj = getattr(module, name)
            if not isinstance(obj, (type, types.FunctionType)):
                continue
            elif obj.__module__ != module.__name__:
                continue
            results.append(obj)
        return results

    def _print_results(self, counts):
        template = stringtools.normalize('''
        Source lines: {source_lines}
        Public classes: {public_classes}
            Unique public methods: {unique_public_methods}
            Unique public properties: {unique_public_properties}
            Unique private methods: {unique_private_methods}
            Unique private properties: {unique_private_properties}
        Public functions: {public_functions}
        Private classes: {private_classes}
        Private functions: {private_functions}
        ''')
        result = template.format(
            source_lines=counts['source_lines'],
            public_classes=counts['public_classes'],
            unique_public_methods=counts['unique_public_methods'],
            unique_public_properties=counts['unique_public_properties'],
            unique_private_methods=counts['unique_private_methods'],
            unique_private_properties=counts['unique_private_properties'],
            public_functions=counts['public_functions'],
            private_classes=counts['private_classes'],
            private_functions=counts['private_functions'],
            )
        print(result)

    def _setup_counts(self):
        counts = {
            'source_lines': 0,
            'private_classes': 0,
            'private_functions': 0,
            'public_classes': 0,
            'public_functions': 0,
            'unique_public_methods': 0,
            'unique_public_properties': 0,
            'unique_private_methods': 0,
            'unique_private_properties': 0,
            }
        return counts

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        from abjad.tools import documentationtools
        path = args.path
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        counts = self._setup_counts()
        for module in documentationtools.yield_all_modules(
            code_root=path,
            ignored_file_names=[],
            ):
            with open(module.__file__, 'r') as file_pointer:
                contents = file_pointer.read()
                counts['source_lines'] += contents.count('\n')
            for obj in self._iterate_module(module):
                if isinstance(obj, types.FunctionType):
                    if obj.__name__.startswith('_'):
                        counts['private_functions'] += 1
                    else:
                        counts['public_functions'] += 1
                elif isinstance(obj, type):
                    if obj.__name__.startswith('_'):
                        counts['private_classes'] += 1
                    else:
                        counts['public_classes'] += 1
                        for attr in inspect.classify_class_attrs(obj):
                            if attr.defining_class != obj:
                                continue
                            if attr.kind in ('method', 'class method', 'static method'):
                                if attr.name.startswith('_'):
                                    counts['unique_private_methods'] += 1
                                else:
                                    counts['unique_public_methods'] += 1
                            elif attr.kind in ('property,'):
                                if attr.name.startswith('_'):
                                    counts['unique_private_properties'] += 1
                                else:
                                    counts['unique_public_properties'] += 1

        self._print_results(counts)

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )
