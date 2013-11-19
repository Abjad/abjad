# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class IndicatorWrapper(AbjadObject):
    r'''An indicator wrapper.
    '''

    ### INITIALIZER ###

    def __init__(self, indicator, start_component, scope=None):
        self._indicator = indicator
        self._start_component = start_component
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
        r'''Indicator of indicator wrapper.

        Returns indicator.
        '''
        return self._indicator

    @property
    def scope(self):
        r'''Target context of indicator wrapper.

        Returns context.
        '''
        return self._scope

    @property
    def start_component(self):
        r'''Start component of indicator wrapper.

        Returns component.
        '''
        return self._start_component
