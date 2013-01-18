import abc
import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


class Setting(AbjadObject):
    r'''Setting.

    Abstract setting class from which concrete settings inherit.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    # TODO: eventually remove 'truncate' in favor of SingleContextDivisionSetting.truncate
    @abc.abstractmethod
    def __init__(self, attribute=None, expression=None, anchor=None, fresh=True, persist=True, truncate=None):
        from experimental.tools import requesttools
        from experimental.tools import settingtools
        from experimental.tools import settingtools
        assert isinstance(attribute, str)
        assert isinstance(expression, (settingtools.Expression)), repr(expression)
        #assert isinstance(anchor, (settingtools.TimespanExpression, str, type(None)))
        assert isinstance(anchor, (settingtools.Expression, str, type(None)))
        assert isinstance(fresh, bool)
        assert isinstance(persist, bool)
        assert isinstance(truncate, (bool, type(None)))
        self._attribute = attribute
        self._expression = expression
        self._anchor = anchor
        self._fresh = fresh
        self._persist = persist
        self._truncate = truncate

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

    def _set_start_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, str)
        if isinstance(self.anchor, str):
            self._anchor = segment_identifier
        else:
            #self.anchor._set_start_segment_identifier(segment_identifier)
            anchor = copy.deepcopy(self.anchor)
            anchor._set_start_segment_identifier(segment_identifier)
            self._anchor = anchor

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Setting anchor.

        Return anchor or none.
        '''
        return self._anchor

    @property
    def attribute(self):
        '''Setting attribute.

        Return string.
        '''
        return self._attribute

    @property
    def fresh(self):
        '''True when setting results from explicit composer command.
        Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def persist(self):
        '''True when setting should persist.
         
        Return boolean.
        '''
        return self._persist

    @property
    def expression(self):
        '''Setting expression.

        Return expression.
        '''
        return self._expression

    @property
    def truncate(self):
        '''True when setting should truncate.

        Return boolean.
        '''
        return self._truncate
