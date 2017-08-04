# -*- coding: utf-8 -*-
import copy
from abjad.tools.abctools import AbjadValueObject


class IndicatorWrapper(AbjadValueObject):
    r'''Indicator wrapper.

    ..  container:: example

        ::

            >>> component = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', Up)
            >>> abjad.annotate(component, 'foo', articulation)
            >>> agent = abjad.inspect(component)
            >>> wrapper = agent.get_indicators(unwrap=False)[0]

        ::

            >>> f(wrapper)
            systemtools.IndicatorWrapper(
                component=abjad.Note("c'4"),
                indicator=abjad.Articulation('accent', Up),
                is_annotation=True,
                name='foo',
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_component',
        '_effective_context',
        '_indicator',
        '_is_annotation',
        '_is_piecewise',
        '_name',
        '_piecewise_spanner',
        '_scope',
        '_synthetic_offset',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        indicator=None,
        is_annotation=None,
        is_piecewise=None,
        name=None,
        piecewise_spanner=None,
        scope=None,
        synthetic_offset=None,
        ):
        import abjad
        assert not isinstance(indicator, type(self)), repr(indicator)
        if component is not None:
            prototype = (abjad.Component, abjad.Spanner)
            assert isinstance(component, prototype)
        self._component = component
        self._effective_context = None
        self._indicator = indicator
        if is_annotation is not None:
            is_annotation = bool(is_annotation)
        self._is_annotation = is_annotation
        if is_piecewise is not None:
            is_piecewise = bool(is_piecewise)
        self._is_piecewise = is_piecewise
        if name is not None:
            name = str(name)
        self._name = name
        if piecewise_spanner is not None:
            assert isinstance(piecewise_spanner, abjad.Spanner)
        self._piecewise_spanner = piecewise_spanner
        if scope is not None:
            if isinstance(scope, type):
                assert issubclass(scope, abjad.Component)
            else:
                assert isinstance(scope, (abjad.Component, str))
        self._scope = scope
        if synthetic_offset is not None:
            synthetic_offset = abjad.Offset(synthetic_offset)
        self._synthetic_offset = synthetic_offset

    ### SPECIAL METHODS ###

    def __copy__(self):
        r'''Copies indicator wrapper.

        ..  container:: example

            Preserves annotation flag:

            ::

                >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
                >>> abjad.annotate(old_staff[0], 'bow_direction', Down)
                >>> f(old_staff)
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> leaf = old_staff[0]
                >>> abjad.inspect(leaf).get_annotation('bow_direction')
                Down

            ::

                >>> new_staff = abjad.mutate(old_staff).copy()
                >>> f(new_staff)
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> leaf = new_staff[0]
                >>> abjad.inspect(leaf).get_annotation('bow_direction')
                Down

        ..  container:: example

            Preserves piecewise flag:

            ::

                >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
                >>> spanner = abjad.TextSpanner()
                >>> abjad.attach(spanner, old_staff[:])
                >>> spanner.attach(abjad.Markup('pont.'), old_staff[0])
                >>> f(old_staff)
                \new Staff {
                    c'4 ^ \markup { pont. }
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> leaf = old_staff[0]
                >>> wrapper = abjad.inspect(leaf).get_indicator(unwrap=False)
                >>> f(wrapper)
                systemtools.IndicatorWrapper(
                    component=abjad.Note("c'4 ^ \\markup { pont. }"),
                    indicator=abjad.Markup(
                        contents=['pont.'],
                        ),
                    is_piecewise=True,
                    piecewise_spanner=spannertools.TextSpanner(),
                    )

            ::

                >>> new_staff = abjad.mutate(old_staff).copy()
                >>> f(new_staff)
                \new Staff {
                    c'4 ^ \markup { pont. }
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> leaf = new_staff[0]
                >>> wrapper = abjad.inspect(leaf).get_indicator(unwrap=False)
                >>> f(wrapper)
                systemtools.IndicatorWrapper(
                    component=abjad.Note("c'4 ^ \\markup { pont. }"),
                    indicator=abjad.Markup(
                        contents=['pont.'],
                        ),
                    is_piecewise=True,
                    )

        Copies indicator and scope.
        
        Does not copy start component.

        Does not copy piecewise spanner.

        This is to avoid reference problems.
        
        Returns new indicator wrapper.
        '''
        new = type(self)(
            component=None,
            indicator=copy.copy(self.indicator),
            is_annotation=self.is_annotation,
            is_piecewise=self.is_piecewise,
            name=self.name,
            scope=self.scope,
            synthetic_offset=self.synthetic_offset,
            )
        return new

    ### PRIVATE METHODS ###

    def _bind_correct_effective_context(self, correct_effective_context):
        import abjad 
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        if isinstance(self.indicator, abjad.MetronomeMark):
            correct_effective_context._update_later(offsets_in_seconds=True)

    def _bind_to_component(self, component):
        import abjad
        self._warn_duplicate_indicator(component)
        self._unbind_component()
        self._component = component
        self._update_effective_context()
        if isinstance(self.indicator, abjad.MetronomeMark):
            self._component._update_later(offsets_in_seconds=True)
        component._indicator_wrappers.append(self)

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
        import abjad
        result = []
        if self.is_annotation:
            return result
        if hasattr(self.indicator, '_get_lilypond_format_bundle'):
            return self.indicator._get_lilypond_format_bundle(self.component)
        lilypond_format = self.indicator._get_lilypond_format()
        if isinstance(lilypond_format, (tuple, list)):
            result.extend(lilypond_format)
        else:
            result.append(lilypond_format)
        if self._get_effective_context() is not None:
            return result
        if isinstance(self.indicator, abjad.TimeSignature):
            if isinstance(self.component, abjad.Measure):
                return result
        result = [r'%%% {} %%%'.format(x) for x in result]
        return result

    def _is_formattable_for_component(self, component):
        import abjad
        if self.is_annotation:
            return False
        if isinstance(self.component, abjad.Measure):
            if self.component is component:
                if not isinstance(self.indicator, abjad.TimeSignature):
                    return True
                elif component.always_format_time_signature:
                    return True
                else:
                    previous_measure = self.component._get_previous_measure()
                    if previous_measure is not None:
                        previous_effective_time_signature = \
                            previous_measure.time_signature
                    else:
                        previous_effective_time_signature = None
                    if not self.indicator == previous_effective_time_signature:
                        return True
        elif getattr(self.indicator, '_format_slot', None) == 'right':
            if self.component is component:
                return True
        elif self.component is component:
            return True
        return False

    def _unbind_component(self):
        component = self.component
        if component is not None:
            if hasattr(component, '_indicator_wrappers'):
                if self in component._indicator_wrappers:
                    component._indicator_wrappers.remove(self)
        self._component = None

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

    def _warn_duplicate_indicator(self, component):
        import abjad
        if isinstance(component, abjad.Spanner):
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
        r'''Gets start component of indicator wrapper.

        Returns component.
        '''
        import abjad
        if isinstance(self._component, abjad.Spanner):
            if self._component:
                return self._component[0]
            else:
                return
        return self._component

    @property
    def indicator(self):
        r'''Gets indicator of indicator wrapper.

        Returns indicator.
        '''
        return self._indicator

    @property
    def is_annotation(self):
        r'''Is true if indicator wrapper is annotation.

        Returns true or false.
        '''
        return self._is_annotation

    @property
    def is_piecewise(self):
        r'''Is true if indicator wrapper is piecewise.

        Returns true or false.
        '''
        return self._is_piecewise

    @property
    def name(self):
        r'''Gets name of indicator wrapper.

        ..  container:: example

            ::

                >>> component = abjad.Note("c'4")
                >>> articulation = abjad.Articulation('accent', Up)
                >>> abjad.attach(articulation, component)
                >>> wrapper = abjad.inspect(component).get_indicators(unwrap=False)[0]
                >>> wrapper.name is None
                True

        ..  container:: example

            ::

                >>> component = abjad.Note("c'4")
                >>> articulation = abjad.Articulation('accent', Up)
                >>> abjad.annotate(component, 'foo', articulation)
                >>> wrapper = abjad.inspect(component).get_indicators(unwrap=False)[0]
                >>> wrapper.name
                'foo'

        ..  container:: example

            ::

                >>> leaf_a = abjad.Note("c'4")
                >>> articulation = abjad.Articulation('accent', Up)
                >>> abjad.attach(articulation, leaf_a)
                >>> wrapper_a = abjad.inspect(leaf_a).get_indicators(unwrap=False)[0]
                >>> wrapper_a.name is None
                True

            ::

                >>> leaf_b = abjad.Note("g'4")
                >>> abjad.attach(wrapper_a, leaf_b)
                >>> wrapper_b = abjad.inspect(leaf_b).get_indicators(unwrap=False)[0]
                >>> wrapper_a is not wrapper_b
                True
                >>> wrapper_b.name is None
                True

        ..  container:: example

            ::

                >>> leaf_a = abjad.Note("c'4")
                >>> articulation = abjad.Articulation('accent', Up)
                >>> abjad.annotate(leaf_a, 'foo', articulation)
                >>> wrapper_a = abjad.inspect(leaf_a).get_indicators(unwrap=False)[0]
                >>> wrapper_a.name == 'foo'
                True

            ::

                >>> leaf_b = abjad.Note("g'4")
                >>> abjad.attach(wrapper_a, leaf_b)
                >>> wrapper_b = abjad.inspect(leaf_b).get_indicators(unwrap=False)[0]
                >>> wrapper_a is not wrapper_b
                True
                >>> wrapper_b.name
                'foo'

        ..  container:: example

            ::

                >>> leaf_a = abjad.Note("c'4")
                >>> articulation = abjad.Articulation('accent', Up)
                >>> abjad.annotate(leaf_a, 'foo', articulation)
                >>> wrapper_a = abjad.inspect(leaf_a).get_indicators(unwrap=False)[0]
                >>> wrapper_a.name
                'foo'

            ::

                >>> leaf_b = abjad.Note("g'4")
                >>> abjad.annotate(leaf_b, 'bar', articulation)
                >>> wrapper_b = abjad.inspect(leaf_b).get_indicators(unwrap=False)[0]
                >>> wrapper_a is not wrapper_b
                True
                >>> wrapper_b.name
                'bar'

        Returns string or none.
        '''
        return self._name

    @property
    def piecewise_spanner(self):
        r'''Gets piecewise spanner of indicator wrapper.

        Returns spanner or none.
        '''
        return self._piecewise_spanner

    @property
    def scope(self):
        r'''Gets scope of indicator wrapper.

        Returns context.
        '''
        return self._scope

    @property
    def start_offset(self):
        r'''Gets start offset of indicator wrapper.

        This is either the wrapper's synthetic offset or the start offset of
        the wrapper's component.

        Returns offset.
        '''
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        return self._component._get_timespan().start_offset

    @property
    def synthetic_offset(self):
        r'''Gets synthetic offset of indicator wrapper.

        Synthetic offset is optional.

        Returns offset or none.
        '''
        return self._synthetic_offset
