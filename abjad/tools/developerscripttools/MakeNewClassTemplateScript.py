# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class MakeNewClassTemplateScript(DeveloperScript):
    r'''Creates class stubs and test subdirectory.

    ..  shell::

        ajv new class --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'class'``.
        '''
        return 'class'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns ``'new'``.
        '''
        return 'new'

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Make a new class template file.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PRIVATE METHODS ###

    def _get_class_names_in_tools_package(self, root, tools_package_name):
        path = os.path.join(root, tools_package_name)
        generator = documentationtools.yield_all_classes(
            code_root=path,
            include_private_objects=True,
            )
        return tuple(sorted(generator, key=lambda x: x.__name__))

    def _get_class_text(self, class_name):
        return [
            '# -*- encoding: utf-8 -*-',
            'from abjad.tools.abctools import AbjadObject',
            '',
            '',
            'class {}(AbjadObject):'.format(class_name),
            '    pass'
            ]

    def _get_tools_package_names(self, root):
        names = []
        for x in os.listdir(root):
            if os.path.isdir(os.path.join(root, x)):
                if not x.startswith(('_', '.')):
                    names.append(x)
        return tuple(sorted(names))

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        from abjad import abjad_configuration
        if args.name.count('.') != 1:
            message = 'not in tools_package.class_name format: {!r}.'
            message = message.format(args.name)
            raise SystemExit(message)
        root_directory = args.path
        tools_package_name, class_name = args.name.split('.')
        if tools_package_name not in self._get_tools_package_names(
            root_directory):
            message = '{!r} is not a valid tools package.'
            message = message.format(tools_package_name)
            raise SystemExit(message)
        if class_name in self._get_class_names_in_tools_package(
            root_directory, tools_package_name):
            message = '{!r} already exists in {!r}'
            message = message.format(class_name, tools_package_name)
            raise SystemExit(message)
        tools_package_directory = os.path.join(
            root_directory,
            tools_package_name,
            )
        if args.path == os.path.join(
            abjad_configuration.abjad_experimental_directory, 'tools'):
            package_root_name = 'experimental'
        elif args.path == os.path.join(
            abjad_configuration.abjad_directory, 'tools'):
            package_root_name = 'abjad'
        else:
            raise SystemExit
        module_file_path = os.path.join(
            tools_package_directory,
            '{}.py'.format(class_name),
            )
        module_text = '\n'.join(self._get_class_text(class_name)) + '\n'
        with open(module_file_path, 'w') as f:
            f.write(module_text)

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''

        from abjad import abjad_configuration
        parser.add_argument('name',
            help='tools package qualified class name'
            )
        path_group = parser.add_mutually_exclusive_group(required=True)
        path_group.add_argument('-X', '--experimental',
            action='store_const',
            const=os.path.join(
                abjad_configuration.abjad_experimental_directory,
                'tools'),
            dest='path',
            help='use the Abjad experimental tools path',
            )
        path_group.add_argument('-M', '--mainline',
            action='store_const',
            const=os.path.join(
                abjad_configuration.abjad_directory, 'tools'),
            dest='path',
            help='use the Abjad mainline tools path',
            )