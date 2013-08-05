# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class SimultaneousSelection(Selection):
    r'''SliceSelection of components taken simultaneously.

    Simultaneously selections implement no duration properties.
    '''

    ### PUBLIC METHODS ###

    def select_vertical_moment_at(self, offset):
        r'''Select vertical moment at `offset`.
        '''
        from abjad.tools import componenttools
        return componenttools.VerticalMoment(self, offset)
