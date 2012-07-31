from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class Setting(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract setting class from which concrete settings inherit.
    '''

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, attribute, source, target, persist=True, truncate=False):
        from experimental import selectortools
        assert isinstance(attribute, str)
        assert isinstance(target, (selectortools.Selector, type(None)))
        assert isinstance(persist, bool)
        assert isinstance(truncate, bool)
        self._attribute = attribute
        self._source = source
        self._target = target
        self._persist = persist
        self._truncate = truncate

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Setting attribute.

        Return string.
        '''
        return self._attribute

    @property
    def persist(self):
        '''True when setting should persist.
         
        Return boolean.
        '''
        return self._persist

    @property
    def source(self):
        '''Setting source.

        Many different return types are possible.
        '''
        return self._source

    @property
    def target(self):
        '''Setting target.

        Return selector or none.
        '''
        return self._target

    @property
    def truncate(self):
        '''True when setting should truncate.

        Return boolean.
        '''
        return self._truncate
