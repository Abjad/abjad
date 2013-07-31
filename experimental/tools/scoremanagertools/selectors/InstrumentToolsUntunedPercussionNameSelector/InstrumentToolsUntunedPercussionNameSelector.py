# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class InstrumentToolsUntunedPercussionNameSelector(Selector):

    ### CLASS ATTRIBUES ###

    space_delimited_lowercase_target_name = 'untuned percussion'

    ### PUBLIC METHODS ###

    def list_items(self):
        return instrumenttools.UntunedPercussion.known_untuned_percussion[:]
