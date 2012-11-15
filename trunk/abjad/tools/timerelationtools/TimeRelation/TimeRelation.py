import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeRelation(AbjadObject):
    r'''.. versionadded:: 2.11

    Object-oriented time relation.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, template):
        assert isinstance(template, str)
        self._template = template

    ### PRIVATE METHODS ###

    # TODO: maybe replace with self._get_expr_offsets()
    def _get_expr_start(self, expr, score_specification=None, context_name=None):
        if hasattr(expr, 'start_offset'):
            return expr.start_offset
        #elif hasattr(expr, 'get_start_offset'):
        #    return expr.get_start_offset(score_specification, context_name)
        elif hasattr(expr, 'get_offsets'):
            return expr.get_offsets(score_specification, context_name)[0]
        else:
            raise ValueError

    # TODO: maybe replace with self._get_expr_offsets()
    def _get_expr_stop(self, expr, score_specification=None, context_name=None):
        if hasattr(expr, 'stop_offset'):
            return expr.stop_offset
        #elif hasattr(expr, 'get_stop_offset'):
        #    return expr.get_stop_offset(score_specification, context_name)
        elif hasattr(expr, 'get_offsets'):
            return expr.get_offsets(score_specification, context_name)[-1]
        else:
            raise ValueError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_fully_loaded(self):
        pass

    @property
    def template(self):
        '''Time relation template.

        Return string.
        '''
        return self._template
