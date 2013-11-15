# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class IndicatorExpression(AbjadObject):
    r'''An indicator expression.
    '''

    ### INITIALIZER ###

    def __init__(self, indicator, target_context=None):
        self._indicator = indicator
        self._target_context = target_context

    ### PUBLIC PROPERTIES ###

    @property
    def indicator(self):
        r'''Indicator of indicator expression.

        Returns indicator.
        '''
        return self._indicator

    @property
    def target_context(self):
        r'''Target context of indicator expression.

        Returns context.
        '''
        return self._target_context
