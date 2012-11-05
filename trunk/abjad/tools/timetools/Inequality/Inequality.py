import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Inequality(AbjadObject):
    r'''.. versionadded:: 2.11

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

    def _get_expr_start(self, expr, score_specification=None, context_name=None):
        if hasattr(expr, 'start_offset'):
            return expr.start_offset
        elif hasattr(expr, 'get_score_start_offset'):
            return expr.get_score_start_offset(score_specification, context_name)
        else:
            raise ValueError

    def _get_expr_stop(self, expr, score_specification=None, context_name=None):
        if hasattr(expr, 'stop_offset'):
            return expr.stop_offset
        elif hasattr(expr, 'get_score_stop_offset'):
            return expr.get_score_stop_offset(score_specification, context_name)
        else:
            raise ValueError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_fully_loaded(self):
        pass

    @property
    def template(self):
        '''Template of time-object inequality.

        Return string.
        '''
        return self._template
