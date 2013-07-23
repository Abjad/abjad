from abjad.tools import contexttools
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ClefNameSelector(Selector):

    ### PUBLIC METHODS ###

    def list_items(self):
        return contexttools.ClefMark.list_clef_names()
