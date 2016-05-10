# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import webbrowser
from abjad.tools import systemtools
from abjad.tools.documentationtools import DocumentationManager
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript


class BuildApiScript(CommandlineScript):
    r'''Builds the Abjad APIs.

    ..  shell::

        ajv api --help

    '''

    ### CLASS VARIABLES ###

    class ExperimentalDocumentationManager(DocumentationManager):
        r'''API generator for the experimental package.
        '''
        api_directory_name = None
        api_title = 'Abjad Experimental API'
        root_package_name = 'experimental'
        source_directory_path_parts = ('docs', 'source')
        tools_packages_package_path = 'experimental.tools'

    class IDEDocumentationManager(DocumentationManager):
        r'''API generator for the Abjad IDE package.
        '''
        api_directory_name = None
        api_title = 'Abjad IDE API'
        root_package_name = 'ide'
        source_directory_path_parts = ('docs', 'source')
        tools_packages_package_path = 'ide.tools'

    class ScoreLibraryDocumentationManager(DocumentationManager):
        r'''API generator for score library documentation.
        '''
        api_directory_name = None
        root_package_name = None
        source_directory_path_parts = None
        tools_packages_package_path = None

        def __init__(
            self,
            api_title,
            docs_directory,
            packages_to_document,
            ):
            self.api_title = api_title
            self.docs_directory = docs_directory
            self.packages_to_document = packages_to_document

    alias = 'api'
    short_description = 'Build the Abjad APIs.'

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
        api_generator.execute()
        if rst_only:
            return
        message = 'Now building the {} {} docs ...'
        message = message.format(api_title, api_format.upper())
        print(message)
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
        api_generator = BuildApiScript.ExperimentalDocumentationManager()
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
        import ide
        api_generator = BuildApiScript.IDEDocumentationManager()
        api_title = 'Abjad IDE'
        docs_directory = os.path.join(
            ide.__path__[0],
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
            ide.__path__[0],
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
        api_generator = DocumentationManager()
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

    def _build_score_library_api(
        self,
        api_title,
        docs_directory,
        packages_to_document,
        api_format='html',
        clean=False,
        rst_only=False,
        ):
        api_generator = BuildApiScript.ScoreLibraryDocumentationManager(
            api_title,
            docs_directory,
            packages_to_document,
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
            docs_directory,
            'build',
            'html',
            'index.html',
            )
        return path

    def _process_args(self, args):
        api_format = args.format
        clean = args.clean
        rst_only = args.rst_only
        paths = []
        prototype = (
            args.experimental,
            args.ide,
            args.mainline,
            args.score_library,
            )
        if not any(prototype):
            args.mainline = True
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
        if args.mainline:
            path = self._build_mainline_api(
                api_format=api_format,
                clean=clean,
                rst_only=rst_only,
                )
            paths.append(path)
        if args.score_library:
            messages = [
                'Must specify all of ...',
                '    --api-title',
                '    --docs-directory',
                '    --packages-to-document',
                '... when building -S or --score-library.',
                ]
            if not all((
                args.api_title,
                args.docs_directory,
                args.packages_to_document,
                )):
                for message in messages:
                    print(message)
                return
            path = self._build_score_library_api(
                args.api_title,
                args.docs_directory,
                args.packages_to_document,
                api_format=api_format,
                clean=clean,
                rst_only=rst_only,
                )
        if api_format == 'html' and args.openinbrowser and not rst_only:
            for path in paths:
                if path.startswith('/'):
                    path = 'file://' + path
                webbrowser.open(path)

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            '-C',
            '--clean',
            action='store_true',
            dest='clean',
            help='run "make clean" before building the api',
            )
        parser.add_argument(
            '-I',
            '--ide',
            action='store_true',
            help='build the Abjad IDE API',
            )
        parser.add_argument(
            '-M',
            '--mainline',
            action='store_true',
            help='build the mainline API',
            )
        parser.add_argument(
            '-O',
            '--open',
            action='store_true',
            dest='openinbrowser',
            help='open the docs in a web browser after building',
            )
        parser.add_argument(
            '-R',
            '--rst-only',
            action='store_true',
            dest='rst_only',
            help='generate the ReSt source files but do not build',
            )
        parser.add_argument(
            '-S',
            '--score-library',
            action='store_true',
            help='build score library API',
            )
        parser.add_argument(
            '-X',
            '--experimental',
            action='store_true',
            help='build the experimental API',
            )
        parser.add_argument(
            '--api-title',
            help='title of API',
            ),
        parser.add_argument(
            '--docs-directory',
            help='documentation directory',
            ),
        parser.add_argument(
            '--packages-to-document',
            help='comma-delimited packages list (ex: "foo.tools,bar.tools")',
            ),
        parser.add_argument(
            '--format',
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
