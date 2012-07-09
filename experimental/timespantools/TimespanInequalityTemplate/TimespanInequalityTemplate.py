from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequalityTemplate(AbjadObject):
    r'''.. versionadded:: 1.0

    Relate expression ``expr`` to timespan ``t``.

    Expression starts during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop')
        TimespanInequalityTemplate('t.start <= expr.start < t.stop')

    Expression stops during timespan::

        >>> timespantools.TimespanInequalityTemplate('t.start < expr.stop <= t.stop')
        TimespanInequalityTemplate('t.start < expr.stop <= t.stop')

    Expression both starts and stops during timespan::

        >>> timespantools.TimespanInequalityTemplate('t.start <= expr.start < expr.stop <= t.stop')
        TimespanInequalityTemplate('t.start <= expr.start < expr.stop <= t.stop')
        
    Timepsan objects perform no input checking.

    SingleSourceTimespan objects share qualities with lamba expressions.
    '''

    ### INITIALIZER ###

    def __init__(self, string):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.string == expr.string:
                return True
        return False

    ### PRIVATE METHODS ###

    # do not indent storage format
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(AbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def string(self):
        '''Inequality string assigned by user.
        '''
        return self._string
