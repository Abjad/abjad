# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class IndicatorWrapper(AbjadObject):
    r'''An indicator expression.
    '''

    ### INITIALIZER ###

    def __init__(self, indicator, scope=None):
        self._indicator = indicator
        self._scope = scope

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.indicator == arg.indicator:
                if self.scope == arg.scope:
                    return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def indicator(self):
        r'''Indicator of indicator expression.

        Returns indicator.
        '''
        return self._indicator

    @property
    def scope(self):
        r'''Target context of indicator expression.

        Returns context.
        '''
        return self._scope
