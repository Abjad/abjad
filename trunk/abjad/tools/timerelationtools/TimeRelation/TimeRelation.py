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

    def _get_expr_offsets(self, expr, score_specification=None, context_name=None):
        if hasattr(expr, 'offsets'):
            return expr.offsets
        elif hasattr(expr, 'get_offsets'):
            return expr.get_offsets(score_specification, context_name)
        else:
            raise ValueError('{!r} has neither offsets property nor get_offsets() method.'.format(expr))

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
