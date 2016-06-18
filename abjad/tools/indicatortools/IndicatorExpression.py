# -*- coding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class IndicatorExpression(AbjadValueObject):
    r'''An indicator expression.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component',
        '_effective_context',
        '_indicator',
        '_is_annotation',
        '_name',
        '_scope',
        '_synthetic_offset',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        indicator=None,
        is_annotation=None,
        name=None,
        scope=None,
        synthetic_offset=None,
        ):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        assert not isinstance(indicator, type(self)), repr(indicator)
        if component is not None:
            #assert isinstance(component, scoretools.Component)
            prototype = (scoretools.Component, spannertools.Spanner)
            assert isinstance(component, prototype)
        if scope is not None:
            if isinstance(scope, type):
                assert issubclass(scope, scoretools.Component)
            else:
                assert isinstance(scope, (scoretools.Component, str))
        self._indicator = indicator
        if is_annotation is not None:
            is_annotation = bool(is_annotation)
        self._is_annotation = is_annotation
        self._component = component
        if name is not None:
            name = str(name)
        self._name = name
        self._scope = scope
        self._effective_context = None
        if synthetic_offset is not None:
            synthetic_offset = durationtools.Offset(synthetic_offset)
        self._synthetic_offset = synthetic_offset

    ### SPECIAL METHODS ###

    def __copy__(self):
        r'''Copies indicator expression.

        Note that indicator and scope are copied
        but that start component is not copied.
        This is to avoid start component reference problems.

        Returns new indicator expression.
        '''
        new = type(self)(
            component=None,
            indicator=copy.copy(self.indicator),
            is_annotation=self.is_annotation,
            name=self.name,
            scope=self.scope,
            synthetic_offset=self.synthetic_offset,
            )
        return new

    def __repr__(self):
        '''Gets interpreter representation of indicator expression.

        Returns string.
        '''
        result = '{}({!r}, {!s}, scope={!r}, is_annotation={!r}, name={!r})'
        result = result.format(
            type(self).__name__,
            self.indicator,
            self.component,
            self.scope,
            self.is_annotation,
            self.name,
            )
        return result

    ### PRIVATE METHODS ###

    def _bind_correct_effective_context(self, correct_effective_context):
        from abjad.tools import indicatortools
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_expressions.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        if isinstance(self.indicator, indicatortools.Tempo):
            correct_effective_context._update_later(offsets_in_seconds=True)

    def _bind_to_component(self, component):
        from abjad.tools import indicatortools
        self._warn_duplicate_indicator(component)
        self._unbind_component()
        self._component = component
        self._update_effective_context()
        if isinstance(self.indicator, indicatortools.Tempo):
            self._component._update_later(offsets_in_seconds=True)
        component._indicator_expressions.append(self)

    def _detach(self):
        self._unbind_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
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
                if getattr(component, 'context_name', None) == scope_name:
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
        if self.is_annotation:
            return result
        if hasattr(self.indicator, '_get_lilypond_format_bundle'):
            return self.indicator._get_lilypond_format_bundle(self.component)
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
        if self.is_annotation:
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

    def _unbind_component(self):
        component = self.component
        if component is not None:
            if hasattr(component, '_indicator_expressions'):
                if self in component._indicator_expressions:
                    component._indicator_expressions.remove(self)
        self._component = None

    def _unbind_effective_context(self):
        effective_context = self._effective_context
        if effective_context is not None:
            try:
                effective_context._dependent_expressions.remove(self)
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

    def _warn_duplicate_indicator(self, component):
        from abjad.tools import spannertools
        if isinstance(component, spannertools.Spanner):
            return
        prototype = type(self.indicator)
        effective = component._get_effective(prototype, unwrap=False)
        if (
            effective is not None and
            effective.scope is not None and
            effective.indicator != self.indicator
            ):
            if effective.start_offset == self.start_offset:
                message = 'effective indicator already attached: {!r}.'
                message = message.format(effective)
                raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''Start component of indicator expression.

        Returns component.
        '''
        from abjad.tools import spannertools
        if isinstance(self._component, spannertools.Spanner):
            if self._component:
                return self._component[0]
            else:
                return
        return self._component

    @property
    def indicator(self):
        r'''Indicator of indicator expression.

        Returns indicator.
        '''
        return self._indicator

    @property
    def is_annotation(self):
        r'''Is true if indicator expression is annotative.

        Returns true or false.
        '''
        return self._is_annotation

    @property
    def name(self):
        r'''Indicator expression name.

        Returns string.
        '''
        return self._name

    @property
    def scope(self):
        r'''Target context of indicator expression.

        Returns context.
        '''
        return self._scope

    @property
    def start_offset(self):
        r'''Start offset of indicator expression.

        This is either the expression's synthetic offset or the start offset of
        the expression's component.

        Returns offset.
        '''
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        return self._component._get_timespan().start_offset

    @property
    def synthetic_offset(self):
        r'''Optional synthetic offset.

        Returns offset or None.
        '''
        return self._synthetic_offset
