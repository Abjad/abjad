# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentIdentifierExpression(AbjadObject):
    r'''Segment identifier expression.

    ::

        >>> segment_identifier_expression = \
        ...     musicexpressiontools.SegmentIdentifierExpression("'red' + 3")

    ::

        >>> segment_identifier_expression
        SegmentIdentifierExpression("'red' + 3")

    Delayed evaluation wrapper similar to Mathematica ``Hold[]``.

    Segment identifier expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, string):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when mandatory and keyword arguments compare equal.
        Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    ### PUBLIC PROPERTIES ###

    @property
    def string(self):
        r'''Segment identifier expresion string.

        ::

            >>> segment_identifier_expression.string
            "'red' + 3"

        Returns string.
        '''
        return self._string
