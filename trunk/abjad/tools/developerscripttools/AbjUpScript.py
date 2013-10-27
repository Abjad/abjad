# -*- encoding: utf-8 -*-
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class AbjUpScript(DeveloperScript):
    r'''Run `ajv svn up -R -C`:

    ..  shell::

        ajv up --help

    Return `AbjUpScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'up'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'run `ajv svn up -R -C`'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        from abjad.tools import developerscripttools
        svn_up_script = developerscripttools.SvnUpdateScript()
        svn_up_script(['-R', '-C'])

    def setup_argument_parser(self, parser):
        pass
