from abjad.tools import instrumenttools
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class InstrumentToolsInstrumentNameSelector(Selector):

    ### CLASS VARIABLES ###

    space_delimited_lowercase_target_name = 'instrument'

    ### PUBLIC METHODS ###

    def list_items(self):
        return instrumenttools.list_instrument_names()
