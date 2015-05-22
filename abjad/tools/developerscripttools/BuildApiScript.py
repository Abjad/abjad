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

    ### CLASS VARIABLES ###

    class ExperimentalAPIGenerator(AbjadAPIGenerator):
        r'''API generator for the experimental package.
        '''

        _api_title = 'Abjad Experimental API'

        @property
        def docs_api_index_path(self):
            from abjad import abjad_configuration
            return os.path.join(
                abjad_configuration.abjad_root_directory,
                'experimental',
                'docs',
                'source',
                'index.rst',
                )

        @property
        def path_definitions(self):
            from abjad import abjad_configuration
            tools_code_path = os.path.join(
                abjad_configuration.abjad_root_directory,
                'experimental',
                'tools',
                )
            tools_docs_path = os.path.join(
                abjad_configuration.abjad_root_directory,
                'experimental',
                'docs',
                'source',
                'tools',
                )
            tools_package_prefix = 'experimental.tools.'
            tools_triple = (
                tools_code_path,
                tools_docs_path,
                tools_package_prefix,
                )
            demos_code_path = os.path.join(
                abjad_configuration.abjad_root_directory,
                'experimental',
                'demos',
                )
            demos_docs_path = os.path.join(
                abjad_configuration.abjad_root_directory,
                'experimental',
                'docs',
                'source',
                'demos',
                )
            demos_package_prefix = 'experimental.demos.'
            demos_triple = (
                demos_code_path,
                demos_docs_path,
                demos_package_prefix,
                )
            all_triples = (tools_triple, demos_triple)
            return all_triples

        @property
        def root_package(self):
            return 'experimental'

        @property
        def tools_package_path_index(self):
            return 2

    class AbjadIDEAPIGenerator(AbjadAPIGenerator):
        r'''API generator for the Abjad IDE package.
        '''

        _api_title = 'Abjad IDE API'

        @property
        def docs_api_index_path(self):
            from abjad import abjad_configuration
            return os.path.join(
                abjad_configuration.score_manager_root_directory,
                'ide',
                'docs',
                'source',
                'index.rst',
                )

        @property
        def path_definitions(self):
            from abjad import abjad_configuration
            code_path = os.path.join(
                abjad_configuration.score_manager_root_directory,
                'ide',
                )
            docs_path = os.path.join(
                abjad_configuration.score_manager_root_directory,
                'ide',
                'docs',
                'source',
                )
            package_prefix = 'ide.'
            triple = (code_path, docs_path, package_prefix)
            all_triples = (triple,)
            return all_triples

        @property
        def root_package(self):
            return 'ide'

        @property
        def tools_package_path_index(self):
            return 1

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

    def _build_api(
        self,
        docs_directory=None,
        api_generator=None,
        api_title=None,
        api_format='html',
        clean=False,
        rst_only=False,
        ):
        api_generator(verbose=True)
        if rst_only:
            return
        print('Now building the {} {} docs ...'.format(
            api_title,
            api_format.upper(),
            ))
        print('')
        with systemtools.TemporaryDirectoryChange(docs_directory):
            if clean:
                print('Cleaning build directory ...')
                command = 'make clean'
                systemtools.IOManager.spawn_subprocess(command)
            if format == 'coverage':
                command = 'sphinx-build -b coverage {} {}'.format(
                    'source',
                    os.path.join('build', 'coverage'),
                    )
                systemtools.IOManager.spawn_subprocess(command)
            else:
                command = 'make {}'.format(api_format)
                systemtools.IOManager.spawn_subprocess(command)

    def _build_experimental_api(
        self,
        api_format='html',
        clean=False,
        rst_only=False,
        ):
        from abjad import abjad_configuration
        api_generator = BuildApiScript.ExperimentalAPIGenerator()
        api_title = 'experimental'
        docs_directory = os.path.join(
            abjad_configuration.abjad_root_directory,
            'experimental',
            'docs',
            )
        self._build_api(
            api_generator=api_generator,
            api_title=api_title,
            api_format=api_format,
            clean=clean,
            docs_directory=docs_directory,
            rst_only=rst_only,
            )
        path = os.path.join(
            abjad_configuration.abjad_root_directory,
            'experimental',
            'docs',
            'build',
            'html',
            'index.html',
            )
        return path

    def _build_ide_api(
        self,
        api_format='html',
        clean=False,
        rst_only=False,
        ):
        from abjad import abjad_configuration
        api_generator = BuildApiScript.AbjadIDEAPIGenerator()
        api_title = 'Abjad IDE'
        docs_directory = os.path.join(
            abjad_configuration.score_manager_root_directory,
            'ide',
            'docs',
            )
        self._build_api(
            api_generator=api_generator,
            api_title=api_title,
            api_format=api_format,
            clean=clean,
            docs_directory=docs_directory,
            rst_only=rst_only,
            )
        path = os.path.join(
            abjad_configuration.score_manager_root_directory,
            'ide',
            'docs',
            'build',
            'html',
            'index.html',
            )
        return path

    def _build_mainline_api(
        self,
        api_format='html',
        clean=False,
        rst_only=False,
        ):
        from abjad import abjad_configuration
        api_generator = AbjadAPIGenerator()
        api_title = 'mainline'
        docs_directory = os.path.join(
            abjad_configuration.abjad_directory,
            'docs',
            )
        self._build_api(
            api_generator=api_generator,
            api_title=api_title,
            api_format=api_format,
            clean=clean,
            docs_directory=docs_directory,
            rst_only=rst_only,
            )
        path = os.path.join(
            abjad_configuration.abjad_root_directory,
            'abjad',
            'docs',
            'build',
            'html',
            'api',
            'index.html',
            )
        return path

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        api_format = args.format
        clean = args.clean
        rst_only = args.rst_only
        paths = []
        if args.mainline:
            path = self._build_mainline_api(
                api_format=api_format,
                clean=clean,
                rst_only=rst_only,
                )
            paths.append(path)
        if args.experimental:
            path = self._build_experimental_api(
                api_format=api_format,
                clean=clean,
                rst_only=rst_only,
                )
            paths.append(path)
        if args.ide:
            path = self._build_ide_api(
                api_format=api_format,
                clean=clean,
                rst_only=rst_only,
                )
            paths.append(path)
        if api_format == 'html' and args.openinbrowser and not rst_only:
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
        parser.add_argument('-I', '--ide',
            action='store_true',
            help='build the Abjad IDE API'
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
        parser.add_argument('-R', '--rst-only',
            action='store_true',
            dest='rst_only',
            help='generate the ReSt source files but do not build',
            )
        parser.add_argument('--format',
            choices=(
                'coverage',
                'html',
                'latex',
                'latexpdf',
                ),
            help='Sphinx builder to use',
            metavar='FORMAT',
            )
        parser.set_defaults(format='html')