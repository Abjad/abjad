from abjad.tools import iotools
from abjad.cfg.cfg import ABJADPATH
from abjad.tools.documentationtools import AbjadAPIGenerator
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import os


class BuildAbjadApiScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'abjad'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'build-api'

    @property
    def short_description(self):
        return 'Build the Abjad API.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):

        print args

        AbjadAPIGenerator()(verbose=True)

        # print greeting
        print 'Now building the {} docs ...'.format(args.format.upper())
        print ''

        # change to docs directory because makefile lives there
        docs_directory = os.path.join(ABJADPATH, 'docs')
        os.chdir(docs_directory)

        # optionally, make clean before building
        if args.clean:
            print 'Cleaning build directory ...'
            iotools.spawn_subprocess('make clean')

        # make html docs
        iotools.spawn_subprocess('make {}'.format(args.format))

    def setup_argument_parser(self, parser):

        parser.add_argument('--clean',
            action='store_true',
            dest='clean',
            help='run "make clean" before building the api',
            )

        parser.add_argument('--format',
            choices=('html', 'latex', 'latexpdf'),
            dest='format',
            help='Sphinx builder to use',
            metavar='X',
            )

        parser.set_defaults(format='html')
