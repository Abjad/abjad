# -*- coding: utf-8 -*-
#import copy
#import itertools
#from abjad.tools import datastructuretools
#from abjad.tools import durationtools
#from abjad.tools.topleveltools import attach
#from abjad.tools.topleveltools import iterate
#from abjad.tools.topleveltools import mutate
from abjad.tools.selectiontools.Selection import Selection


class ContiguousSelection(Selection):
    r'''A time-contiguous selection of components.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        music = self._coerce_music(music)
        self._music = tuple(music)