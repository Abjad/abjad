from abjad.tools import abctools


class RotationIndicator(abctools.AbjadObject):
    r'''.. versionadded:: 2.11

    Rotation indicator.
    '''

    def __init__(self, index, level=-1):
        self._index = index
        self._level = level

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def index(self):
        return self._index

    @property
    def level(self):
        return self._level
