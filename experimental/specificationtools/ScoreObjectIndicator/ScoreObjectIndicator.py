from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
import types


class ScoreObjectIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    Frozen request to pick out an arbitrary object in score.

    Initialize with a score segment alone::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.ScoreObjectIndicator(segment='red')
        ScoreObjectIndicator(segment='red')

    This says to pick out the segment with name ``'red'``.

    Initialize with score segment and component class::

        >>> specificationtools.ScoreObjectIndicator(segment='red', klass=Note)
        ScoreObjectIndicator(segment='red', klass=notetools.Note)

    This says to pick out the first note in the segment with name ``'red'``.

    Initialize with score segment, component class and integer index::

        >>> specificationtools.ScoreObjectIndicator(segment='red', klass=Note, index=20)
        ScoreObjectIndicator(segment='red', klass=notetools.Note, index=20)

    This says to pick out note at index ``20`` in the segment with name ``'red'``.

    It is important to note that when ``klass`` is set equal to none that the object
    picked out by the indicator will be entire score segment rather than Abjad component.

    Both `predicate` and `index` are ignored when `klass` is left equal to none.

    Score object indicators are immutable.

    .. note:: context needs to be worked into all of these examples except the first one.
    '''

    ### INITIALIZER ###

    def __init__(self, segment=None, context=None, klass=None, predicate=None, index=None):
        if isinstance(segment, SegmentSpecification):
            segment = segment.name
        assert isinstance(segment, (str, type(None))), repr(segment)
        if isinstance(context, contexttools.Context):
            context = context.name
        assert isinstance(context, (str, type(None))), repr(context)
        if klass is not None:
            assert issubclass(klass, componenttools.Component), repr(klass)
        assert isinstance(predicate, (types.FunctionType, type(None))), repr(predicate)
        assert isinstance(index, (int, type(None))), repr(index)
        self._segment = segment
        self._context = context
        self._klass = klass
        self._predicate = predicate
        self._index = index
    
    ### SPECIAL METHODS ###

#    def __repr__(self):
#        pass

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def context(self):
        return self._context

    @property
    def index(self):
        return self._index

    @property
    def klass(self):
        return self._klass

    @property
    def predicate(self):
        return self._predicate

    @property
    def segment(self):
        return self._segment
