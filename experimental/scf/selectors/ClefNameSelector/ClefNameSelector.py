from abjad.tools import contexttools
from scf.selectors.Selector import Selector


class ClefNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        return contexttools.list_clef_names()
