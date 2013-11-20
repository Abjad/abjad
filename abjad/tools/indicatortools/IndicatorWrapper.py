# -*- encoding: utf-8 -*-
import copy
import types
from abjad.tools.abctools import AbjadObject


# TODO: change IndicatorWrapper.start_component to IndicatorWrapper.component
#       do this after removing ContextMark from codebase
class IndicatorWrapper(AbjadObject):
    r'''An indicator wrapper.
    '''

    ### INITIALIZER ###

    def __init__(self, indicator, start_component, scope=None):
        from abjad.tools import scoretools
        assert not isinstance(indicator, type(self)), repr(indicator)
        assert isinstance(start_component, (scoretools.Component, type(None))), repr(start_component)
        assert scope is None or \
            (isinstance(scope, types.TypeType) and 
            issubclass(scope, scoretools.Component)) or \
            isinstance(scope, scoretools.Component), repr(scope)
        self._indicator = indicator
        self._start_component = start_component
        self._scope = scope
        self._effective_context = None

    ### SPECIAL METHODS ###

    def __copy__(self):
        r'''Copies indicator wrapper.

        Note that indicator and scope are copied
        but that start component is not copied.
        This is to avoid start component reference problems.

        Returns new indicator wrapper.
        '''
        return type(self)(
            copy.copy(self.indicator),
            None,
            scope=self.scope,
            )
            
    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.indicator == arg.indicator:
                if self.scope == arg.scope:
                    return True
        return False

    def __repr__(self):
        '''Interpreter representation of indicator wrapper.

        Returns string.
        '''
        result = '{}({!r}, {!s}, scope={!r})'
        result = result.format(
            type(self).__name__,
            self.indicator,
            self.start_component,
            self.scope,
            )
        return result

    ### PRIVATE METHODS ###

    def _bind_correct_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()

    def _detach(self):
        self._unbind_start_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
        from abjad.tools import scoretools
        scope = self.scope
        if scope is None:
            return None
        elif isinstance(scope, type):
            scope_type = scope
            for component in self.start_component._get_parentage():
                if isinstance(component, scope_type):
                    return component
        elif isinstance(scope, str):
            scope_name = scope
            for component in self.start_component._get_parentage():
                if component.name == scope_name:
                    return component
        else:
            message = 'target context {!r} must be'
            message += ' context type, context name or none.'
            message = message.format(scope)
            raise TypeError(message)

    def _unbind_effective_context(self):
        effective_context = self._effective_context
        if effective_context is not None:
            try:
                effective_context._dependent_wrappers.remove(self)
            except ValueError:
                pass
        self._effective_context = None

    def _update_effective_context(self):
        r'''This function is designed to be called by score components
        during score update.
        '''
        current_effective_context = self._effective_context
        correct_effective_context = self._find_correct_effective_context()
        if current_effective_context is not correct_effective_context:
            self._bind_correct_effective_context(correct_effective_context)

    def _unbind_start_component(self):
        start_component = self.start_component
        if start_component is not None:
            try:
                start_component._indicators.remove(self)
            except ValueError:
                pass
        self._start_component = None

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
