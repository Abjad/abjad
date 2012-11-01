from abjad.tools import abctools


class RotationIndicator(abctools.AbjadObject):
    r'''.. versionadded:: 2.11

    .. note:: add example.

    Rotation indicator.
    '''

    def __init__(self, index, level=None, fracture_spanners=None):
        from abjad.tools import durationtools
        assert isinstance(index, (int, durationtools.Duration))
        assert isinstance(level, (int, type(None)))
        assert isinstance(fracture_spanners, (bool, type(None)))
        self._index = index
        self._level = level
        self._fracture_spanners = fracture_spanners

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def fracture_spanners(self):
        return self._fracture_spanners

    @property
    def index(self):
        return self._index

    @property
    def level(self):
        return self._level
