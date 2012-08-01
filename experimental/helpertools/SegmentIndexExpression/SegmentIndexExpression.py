from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentIndexExpression(AbjadObject):
    r'''.. versionadded:: 1.0

    Delayed evaluation wrapper similar to Mathematica ``Hold[]``::

        >>> from experimental import *

    ::

        >>> helpertools.SegmentIndexExpression("'red' + 3")
        SegmentIndexExpression("'red' + 3")

    Delays evaluation of string argument until later in interpretation.

    Used primarily as arguments to slice selector start and stop keywords.

    All held expression properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, string):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### PRIVATE METHODS ###

    # do not indent storage format
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(AbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def string(self):
        '''String initialized by user.

        Return string.
        '''
        return self._string
