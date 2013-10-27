# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class MakeNewClassTemplateScript(DeveloperScript):
    r'''Create class stubs, complete with test subdirectory:

    ..  shell::

        ajv new class --help

    Return `MakeNewClassTemplateScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'class'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'new'

    @property
    def short_description(self):
        return 'Make a new class template file.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _get___init___text(self, package_root_name):
        return [
            'from abjad.tools import importtools',
            '',
            "importtools.ImportManager.import_structured_package(__path__[0], globals(), package_root_name={!r})".format(package_root_name),
        ]

    def _get_class_names_in_tools_package(self, root, tools_package_name):
        path = os.path.join(root, tools_package_name)
        crawler = documentationtools.ClassCrawler(
            path, include_private_objects=True)
        objs = crawler()
        return tuple(sorted([x.__name__ for x in objs]))

    def _get_class_text(self, class_name):
        return [
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

        from abjad import abjad_configuration

        if args.name.count('.') != 1:
            message = 'Error: {!r} not in tools_package.class_name format.'
            print message.format(args.name)
            return

        root = args.path
        tools_package_name, class_name = args.name.split('.')

        if tools_package_name not in self._get_tools_package_names(root):
            print 'Error: {!r} is not a valid tools package.'.format(
                tools_package_name)
            return

        if class_name in self._get_class_names_in_tools_package(
            root, tools_package_name):
            print 'Error: {!r} already exists in {!r}'.format(
                class_name, tools_package_name)
            return

        package_path = os.path.join(root, tools_package_name, class_name)

        os.mkdir(package_path)
        os.mkdir(os.path.join(package_path, 'test'))

        if args.path == os.path.join(
            abjad_configuration.abjad_experimental_directory_path, 'tools'):
            package_root_name = 'experimental'
        elif args.path == os.path.join(
            abjad_configuration.abjad_directory_path, 'tools'):
            package_root_name = 'abjad'
        else:
            raise Exception

        module_path = os.path.join(package_path, '{}.py'.format(class_name))
        module_text = '\n'.join(self._get_class_text(class_name)) + '\n'

        init_path = os.path.join(package_path, '__init__.py')
        init_text = '\n'.join(self._get___init___text(package_root_name))
        init_text += '\n'

        with open(module_path, 'w') as f:
            f.write(module_text)

        with open(init_path, 'w') as f:
            f.write(init_text)

    def setup_argument_parser(self, parser):

        from abjad import abjad_configuration

        parser.add_argument('name',
            help='tools package qualified class name'
            )

        path_group = parser.add_mutually_exclusive_group(required=True)

        path_group.add_argument('-X', '--experimental',
            action='store_const',
            const=os.path.join(
                abjad_configuration.abjad_experimental_directory_path, 
                'tools'),
            dest='path',
            help='use the Abjad experimental tools path',
            )

        path_group.add_argument('-M', '--mainline',
            action='store_const',
            const=os.path.join(
                abjad_configuration.abjad_directory_path, 'tools'),
            dest='path',
            help='use the Abjad mainline tools path',
            )
