from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextedSelector(AbjadObject):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    Arbitrarily many contexts joined to an arbitrary selector.

    ``ContextedSelector`` objects basically function as a fancy type of pair.

    All ``ContextedSelector`` properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, selector, contexts=None):
        from experimental import selectortools
        assert isinstance(selector, selectortools.Selector), repr(selector)
        assert isinstance(contexts, (list, type(None))), repr(contexts)
        self._selector = selector
        self._contexts = contexts

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contexts(self):
        '''Contexts specified by user.

        Value of none taken equal to all contexts in score.

        Return list of strings or none.
        '''
        return self._contexts

    @property
    def selector(self):
        '''Selector specified by user.

        Return selector.
        '''
        return self._selector
