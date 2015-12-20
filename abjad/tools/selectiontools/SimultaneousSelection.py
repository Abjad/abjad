# -*- coding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class SimultaneousSelection(Selection):
    r'''A selection of components taken simultaneously.

    Simultaneously selections implement no duration properties.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )