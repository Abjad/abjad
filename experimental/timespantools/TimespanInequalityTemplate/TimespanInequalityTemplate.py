from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequalityTemplate(AbjadObject):
    r'''.. versionadded:: 1.0

    Relate expression ``expr`` to timespan ``t``.

        >>> from experimental import *

    Expression starts during timespan::

        >>> timespantools.TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_1.stop')
        TimespanInequality('expr_1.start <= expr_2.start < expr_1.stop')

    Expression stops during timespan::

        >>> timespantools.TimespanInequalityTemplate('expr_1.start < expr_2.stop <= expr_1.stop')
        TimespanInequality('expr_1.start < expr_2.stop <= expr_1.stop')

    Expression both starts and stops during timespan::

        >>> timespantools.TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_2.stop <= expr_1.stop')
        TimespanInequality('expr_1.start <= expr_2.start < expr_2.stop <= expr_1.stop')
        
    Timepsan inequality template objects perform no input checking.

    Timespan inequality template objects are frozen inequalities.
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
