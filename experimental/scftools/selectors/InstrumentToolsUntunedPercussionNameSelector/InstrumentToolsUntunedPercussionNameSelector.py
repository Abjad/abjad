from abjad.tools import instrumenttools
from scftools.selectors.Selector import Selector


class InstrumentToolsUntunedPercussionNameSelector(Selector):

    ### CLASS ATTRIBUES ###

    target_human_readable_name = 'untuned percussion'

    ### PUBLIC METHODS ###

    def list_items(self):
        return instrumenttools.UntunedPercussion.known_untuned_percussion[:]
