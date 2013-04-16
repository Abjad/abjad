from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextProxy(AbjadObject):
    '''Context proxy.
    '''

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import musicexpressiontools
        self._single_context_set_expressions_by_attribute = \
            musicexpressiontools.AttributeDictionary()
        self._timespan_scoped_single_context_set_expressions_by_attribute = \
            musicexpressiontools.AttributeDictionary()
        for attribute in self._timespan_scoped_single_context_set_expressions_by_attribute:
            self._timespan_scoped_single_context_set_expressions_by_attribute[attribute] = \
                musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def single_context_set_expressions_by_attribute(self):
        '''Context proxy single-context set expressions by attribute.

        Return attribute dictionary.
        '''
        return self._single_context_set_expressions_by_attribute

    @property
    def timespan_scoped_single_context_set_expressions_by_attribute(self):
        '''Context proxy timespan-scoped
        single-context set expressions by attribute.

        Return attribute dictionary.
        '''
        return self._timespan_scoped_single_context_set_expressions_by_attribute
