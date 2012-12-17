from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentIdentifierExpression(AbjadObject):
    r'''.. versionadded:: 1.0

    Delayed evaluation wrapper similar to Mathematica ``Hold[]``::

        >>> from experimental.tools import *

    ::

        >>> helpertools.SegmentIdentifierExpression("'red' + 3")
        SegmentIdentifierExpression("'red' + 3")

    Delays evaluation of string argument until later in interpretation.

    Used primarily as arguments to slice selector start and stop keywords.

    All held expression properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, string):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

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
