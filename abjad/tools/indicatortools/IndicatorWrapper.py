# -*- encoding: utf-8 -*-
import copy
import types
from abjad.tools.abctools import AbjadObject


class IndicatorWrapper(AbjadObject):
    r'''An indicator wrapper.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component',
        '_effective_context',
        '_indicator',
        '_scope',
        )

    ### INITIALIZER ###

    def __init__(self, indicator, component, scope=None):
        from abjad.tools import scoretools
        assert not isinstance(indicator, type(self)), repr(indicator)
        if component is not None:
            assert isinstance(component, scoretools.Component)
        if scope is not None:
            if isinstance(scope, types.TypeType):
                assert issubclass(scope, scoretools.Component)
            else:
                assert isinstance(scope, scoretools.Component)
        self._indicator = indicator
        self._component = component
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
        new = type(self)(
            copy.copy(self.indicator),
            None,
            scope=self.scope,
            )
        return new
            
    def __eq__(self, arg):
        r'''True when arg is an indicator wrapper with indicator and
        scope equal to those of this indicator wrapper. Otherwise false.

        Returns boolean.
        '''
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
            self.component,
            self.scope,
            )
        return result

    ### PRIVATE METHODS ###

    def _bind_correct_effective_context(self, correct_effective_context):
        from abjad.tools import indicatortools
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        if isinstance(self.indicator, indicatortools.Tempo):
            correct_effective_context._update_later(offsets_in_seconds=True)

    def _bind_to_component(self, component):
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        assert isinstance(component, scoretools.Component)
        self._warn_duplicate_indicator(component)
        self._unbind_component()
        self._component = component
        self._update_effective_context()
        if isinstance(self.indicator, indicatortools.Tempo):
            self._component._update_later(offsets_in_seconds=True)
        component._indicators.append(self)

    def _detach(self):
        self._unbind_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
        from abjad.tools import scoretools
        scope = self.scope
        if scope is None:
            return None
        elif isinstance(scope, type):
            scope_type = scope
            for component in self.component._get_parentage():
                if isinstance(component, scope_type):
                    return component
        elif isinstance(scope, str):
            scope_name = scope
            for component in self.component._get_parentage():
                if component.name == scope_name:
                    return component
        else:
            message = 'target context {!r} must be'
            message += ' context type, context name or none.'
            message = message.format(scope)
            raise TypeError(message)

    def _get_effective_context(self):
        if self.component is not None:
            self.component._update_now(indicators=True)
        return self._effective_context

    def _get_format_pieces(self):
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        result = []
        lilypond_format = self.indicator._lilypond_format
        if isinstance(lilypond_format, (tuple, list)):
            result.extend(lilypond_format)
        else:
            result.append(lilypond_format)
        if self._get_effective_context() is not None:
            return result
        if isinstance(self.indicator, indicatortools.TimeSignature):
            if isinstance(self.component, scoretools.Measure):
                return result
        result = [r'%%% {} %%%'.format(x) for x in result]
        return result

    def _is_formattable_for_component(self, component):
        from abjad.tools import scoretools
        from abjad.tools import indicatortools
        if not hasattr(self.indicator, '_format_slot'):
            return False
        if isinstance(self.component, scoretools.Measure):
            if self.component is component:
                if not isinstance(
                    self.indicator, indicatortools.TimeSignature):
                    return True
                elif component.always_format_time_signature:
                    return True
                else:
                    previous_measure = \
                        scoretools.get_previous_measure_from_component(
                            self.component)
                    if previous_measure is not None:
                        previous_effective_time_signature = \
                            previous_measure.time_signature
                    else:
                        previous_effective_time_signature = None
                    if not self.indicator == previous_effective_time_signature:
                        return True
        elif self.indicator._format_slot == 'right':
            if self.component is component:
                return True
        elif self.component is component:
            return True
        return False

    def _unbind_effective_context(self):
        effective_context = self._effective_context
        if effective_context is not None:
            try:
                effective_context._dependent_wrappers.remove(self)
            except ValueError:
                pass
        self._effective_context = None

    def _unbind_component(self):
        component = self.component
        if component is not None:
            try:
                component._indicators.remove(self)
            except ValueError:
                pass
        self._component = None

    def _update_effective_context(self):
        r'''This function is designed to be called by score components
        during score update.
        '''
        current_effective_context = self._effective_context
        correct_effective_context = self._find_correct_effective_context()
        if current_effective_context is not correct_effective_context:
            self._bind_correct_effective_context(correct_effective_context)

    def _warn_duplicate_indicator(self, component):
        prototype = type(self.indicator)
        effective = component._get_effective_indicator(prototype, unwrap=False)
        if effective is not None and \
            effective.scope is not None and \
            effective.indicator != self.indicator:
            indicator_start = effective.component._get_timespan().start_offset
            component_start = component._get_timespan().start_offset
            if indicator_start == component_start:
                message = 'effective indicator already attached.'
                raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''Start component of indicator wrapper.

        Returns component.
        '''
        return self._component

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
