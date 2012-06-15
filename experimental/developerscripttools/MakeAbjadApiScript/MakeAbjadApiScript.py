from abjad.tools import iotools
from abjad.cfg.cfg import ABJADPATH
from abjad.tools.documentationtools import AbjadAPIGenerator
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import os


class MakeAbjadApiScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'abjad'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'make-api'

    @property
    def short_description(self):
        return 'Make the Abjad API.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _process_args(self, args):

        AbjadAPIGenerator()(verbose=True)

        # print greeting
        print 'Now building the HTML docs ...'
        print ''

        # change to docs directory because makefile lives there
        docs_directory = os.path.join(ABJADPATH, 'docs')
        os.chdir(docs_directory)

        # make html docs
        iotools.spawn_subprocess('make html')

    def _setup_argument_parser(self, parser):
        pass
