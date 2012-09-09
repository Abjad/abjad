import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeObjectInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Time-object inequality.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, template):
        assert isinstance(template, str)
        self._template = template

    ### PRIVATE METHODS ###

    def _get_expr_start(self, expr):
        if hasattr(expr, 'start_offset'):
            return expr.start_offset
        else:
            raise ValueError

    def _get_expr_stop(self, expr):
        if hasattr(expr, 'stop_offset'):
            return expr.stop_offset
        else:
            raise ValueError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def template(self):
        '''Template of time-object inequality.

        Return string.
        '''
        return self._template
