# -*- encoding: utf-8 -*-
import os
import webbrowser
from abjad.tools import systemtools
from abjad.tools.documentationtools import AbjadAPIGenerator
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class BuildApiScript(DeveloperScript):
    r'''Builds the Abjad APIs.

    ..  shell::

        ajv api --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'api'``.
        '''
        return 'api'

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
        return 'Build the Abjad APIs.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PRIVATE METHODS ###

    def _build_experimental_api(self, format='html', clean=False):

        from abjad import abjad_configuration

        class ExperimentalAPIGenerator(AbjadAPIGenerator):

            _api_title = 'Abjad Experimental API'

            @property
            def docs_api_index_path(self):
                return os.path.join(
                    abjad_configuration.abjad_experimental_directory_path,
                    'docs', 'source', 'index.rst')

            @property
            def path_definitions(self):
                from abjad import abjad_configuration
                return (
                    (
                        os.path.join(
                            abjad_configuration.abjad_experimental_directory_path, 
                            'tools'),
                        os.path.join(
                            abjad_configuration.abjad_experimental_directory_path, 
                            'docs', 'source', 'tools'),
                        'experimental.tools.',
                    ),
                    (
                        os.path.join(
                            abjad_configuration.abjad_experimental_directory_path, 
                            'demos'),
                        os.path.join(
                            abjad_configuration.abjad_experimental_directory_path, 
                            'docs', 'source', 'demos'),
                        'experimental.demos.',
                    ),
                )

            @property
            def root_package(self):
                return 'experimental'

            @property
            def tools_package_path_index(self):
                return 2

        ExperimentalAPIGenerator()(verbose=True)

        # print greeting
        print 'Now building the Experimental {} docs ...'.format(
            format.upper())
        print ''

        # change to docs directory because makefile lives there
        docs_directory = os.path.join(
            abjad_configuration.abjad_experimental_directory_path, 'docs')
        os.chdir(docs_directory)

        # optionally, make clean before building
        if clean:
            print 'Cleaning build directory ...'
            systemtools.IOManager.spawn_subprocess('make clean')

        if format == 'coverage':
            systemtools.IOManager.spawn_subprocess('sphinx-build -b coverage {} {}'.format(
                'source',
                os.path.join('build', 'coverage'),
                ))
        else:
            systemtools.IOManager.spawn_subprocess('make {}'.format(format))

    def _build_mainline_api(self, format='html', clean=False):
        from abjad import abjad_configuration
        AbjadAPIGenerator()(verbose=True)
        # print greeting
        print 'Now building the {} docs ...'.format(format.upper())
        print ''
        # change to docs directory because makefile lives there
        docs_directory = os.path.relpath(os.path.join(
            abjad_configuration.abjad_directory_path, 'docs'))
        os.chdir(docs_directory)
        # optionally, make clean before building
        if clean:
            print 'Cleaning build directory ...'
            systemtools.IOManager.spawn_subprocess('make clean')
        if format == 'coverage':
            systemtools.IOManager.spawn_subprocess('sphinx-build -b coverage {} {}'.format(
                'source',
                os.path.join('build', 'coverage'),
                ))
        else:
            systemtools.IOManager.spawn_subprocess('make {}'.format(format))

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        from abjad import abjad_configuration
        format = args.format
        clean = args.clean
        paths = []
        if args.mainline:
            self._build_mainline_api(format=format, clean=clean)
            paths.append(os.path.abspath(os.path.join(
                abjad_configuration.abjad_directory_path,
                'docs',
                'build',
                'html',
                'api',
                'index.html',
                )))
        if args.experimental:
            self._build_experimental_api(format=format, clean=clean)
            paths.append(os.path.abspath(os.path.join(
                abjad_configuration.abjad_experimental_directory_path,
                'docs',
                'build',
                'html',
                'index.html',
                )))
        if args.format == 'html' and args.openinbrowser:
            for path in paths:
                if path.startswith('/'):
                    path = 'file://' + path
                webbrowser.open(path)

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument('-M', '--mainline',
            action='store_true',
            help='build the mainline API'
            )
        parser.add_argument('-X', '--experimental',
            action='store_true',
            help='build the experimental API'
            )
        parser.add_argument('-C', '--clean',
            action='store_true',
            dest='clean',
            help='run "make clean" before building the api',
            )
        parser.add_argument('-O', '--open',
            action='store_true',
            dest='openinbrowser',
            help='open the docs in a web browser after building',
            )
        parser.add_argument('--format',
            choices=(
                'coverage',
                'html',
                'latex',
                'latexpdf',
                ),
            dest='format',
            help='Sphinx builder to use',
            metavar='FORMAT',
            )
        parser.set_defaults(format='html')
