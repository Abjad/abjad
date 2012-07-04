from abjad.tools import iotools
from abjad.cfg.cfg import EXPERIMENTALPATH
from abjad.tools.documentationtools import AbjadAPIGenerator
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import os


class BuildApiScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'api'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'Build the Abjad APIs.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _build_experimental_api(self, format='html', clean=False):

        class ExperimentalAPIGenerator(AbjadAPIGenerator):

            _api_title = 'Abjad Experimental API'

            @property
            def code_tools_path(self):
                return EXPERIMENTALPATH

            @property
            def docs_api_index_path(self):
                return os.path.join(EXPERIMENTALPATH, 'docs', 'source', 'index.rst')

            @property
            def docs_tools_path(self):
                return os.path.join(EXPERIMENTALPATH, 'docs', 'source', 'experimental')

            @property
            def package_prefix(self):
                return 'experimental.'

            @property
            def root_package(self):
                return 'experimental'

            @property
            def tools_package_path_index(self):
                return 1

        ExperimentalAPIGenerator()(verbose=True)

        # print greeting
        print 'Now building the Experimental {} docs ...'.format(format.upper())
        print ''

        # change to docs directory because makefile lives there
        docs_directory = os.path.join(EXPERIMENTALPATH, 'docs')
        os.chdir(docs_directory)

        # optionally, make clean before building
        if clean:
            print 'Cleaning build directory ...'
            iotools.spawn_subprocess('make clean')

        # make html docs
        iotools.spawn_subprocess('make {}'.format(format))

    def _build_mainline_api(self, format='html', clean=False):

        AbjadAPIGenerator()(verbose=True)

        # print greeting
        print 'Now building the {} docs ...'.format(format.upper())
        print ''

        # change to docs directory because makefile lives there
        docs_directory = os.path.relpath(os.path.join(ABJADPATH, 'docs'))
        os.chdir(docs_directory)

        # optionally, make clean before building
        if clean:
            print 'Cleaning build directory ...'
            iotools.spawn_subprocess('make clean')

        # make html docs
        iotools.spawn_subprocess('make {}'.format(format))

    ### PUBLIC METHODS ###

    def process_args(self, args):
        format = args.format
        clean = args.clean
        if args.mainline:
            self._build_mainline_api(format=format, clean=clean)
        if args.experimental:
            self._build_experimental_api(format=format, clean=clean)

    def setup_argument_parser(self, parser):

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

        parser.add_argument('--format',
            choices=('html', 'latex', 'latexpdf'),
            dest='format',
            help='Sphinx builder to use',
            metavar='FORMAT',
            )

        parser.set_defaults(format='html')
