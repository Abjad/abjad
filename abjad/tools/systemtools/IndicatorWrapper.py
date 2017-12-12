import copy
from abjad.tools.abctools import AbjadValueObject


class IndicatorWrapper(AbjadValueObject):
    r'''Indicator wrapper.

    ..  container:: example

        >>> component = abjad.Note("c'4")
        >>> articulation = abjad.Articulation('accent', abjad.Up)
        >>> abjad.attach(articulation, component)
        >>> agent = abjad.inspect(component)
        >>> wrapper = agent.get_indicators(unwrap=False)[0]

        >>> abjad.f(wrapper)
        abjad.IndicatorWrapper(
            component=abjad.Note("c'4 ^\\accent"),
            indicator=abjad.Articulation('accent', Up),
            )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_component',
        '_context',
        '_effective_context',
        '_indicator',
        '_is_annotation',
        '_is_piecewise',
        '_name',
        '_piecewise_spanner',
        '_synthetic_offset',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        context=None,
        indicator=None,
        is_annotation=None,
        is_piecewise=None,
        name=None,
        piecewise_spanner=None,
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
        if context is not None:
            if isinstance(context, type):
                assert issubclass(context, abjad.Component)
            else:
                assert isinstance(context, (abjad.Component, str))
        self._context = context
        if synthetic_offset is not None:
            synthetic_offset = abjad.Offset(synthetic_offset)
        self._synthetic_offset = synthetic_offset

    ### SPECIAL METHODS ###

    def __copy__(self):
        r'''Copies indicator wrapper.

        ..  container:: example

            Preserves annotation flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.annotate(old_staff[0], 'bow_direction', abjad.Down)
            >>> abjad.f(old_staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> abjad.inspect(leaf).get_annotation('bow_direction')
            Down

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> abjad.inspect(leaf).get_annotation('bow_direction')
            Down

        ..  container:: example

            Preserves piecewise flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, old_staff[:])
            >>> spanner.attach(abjad.Markup('pont.'), old_staff[0])
            >>> abjad.f(old_staff)
            \new Staff {
                c'4 ^ \markup { pont. }
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).get_indicator(unwrap=False)
            >>> abjad.f(wrapper)
            abjad.IndicatorWrapper(
                component=abjad.Note("c'4 ^ \\markup { pont. }"),
                indicator=abjad.Markup(
                    contents=['pont.'],
                    ),
                is_piecewise=True,
                piecewise_spanner=abjad.TextSpanner(),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                c'4 ^ \markup { pont. }
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).get_indicator(unwrap=False)
            >>> abjad.f(wrapper)
            abjad.IndicatorWrapper(
                component=abjad.Note("c'4 ^ \\markup { pont. }"),
                indicator=abjad.Markup(
                    contents=['pont.'],
                    ),
                is_piecewise=True,
                )

        Copies indicator and context.

        Does not copy start component.

        Does not copy piecewise spanner.

        This is to avoid reference problems.

        Returns new indicator wrapper.
        '''
        new = type(self)(
            component=None,
            context=self.context,
            indicator=copy.copy(self.indicator),
            is_annotation=self.is_annotation,
            is_piecewise=self.is_piecewise,
            name=self.name,
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
        import abjad
        context = self.context
        if context is None:
            return None
        if isinstance(context, str):
            if hasattr(abjad, context):
                context = getattr(abjad, context)
        if isinstance(context, type):
            context_type = context
            for component in abjad.inspect(self.component).get_parentage():
                if isinstance(component, context_type):
                    return component
        elif isinstance(context, str):
            context_name = context
            for component in abjad.inspect(self.component).get_parentage():
                if getattr(component, 'context_name', None) == context_name:
                    return component
        else:
            message = '{!r} must be context type, context name or none.'
            message = message.format(context)
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
        try:
            context = self._get_effective_context()
            lilypond_format = self.indicator._get_lilypond_format(
                context=context,
                )
        except TypeError:
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
        result = [r'%%% {} %%%'.format(_) for _ in result]
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
        wrapper = component._get_effective(prototype, unwrap=False)
        if (wrapper is not None and
            wrapper.context is not None and
            wrapper.indicator != self.indicator):
            if wrapper.start_offset == self.start_offset:
                message = 'can not attach {} to ...\n\n{}'
                message += '\n\n... because {} is already attached to ...\n\n'
                message += '{}\n\nsee wrapper: {!r}.'
                message = message.format(
                    self.indicator,
                    component,
                    wrapper.indicator,
                    wrapper.component,
                    wrapper,
                    )
                raise Exception(message)

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
    def context(self):
        r'''Gets context of indicator wrapper.

        Returns context or string.
        '''
        return self._context

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

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', abjad.Up)
            >>> abjad.attach(articulation, note)
            >>> agent = abjad.inspect(note)
            >>> wrapper = agent.get_indicators(unwrap=False)[0]
            >>> wrapper.name is None
            True

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', abjad.Up)
            >>> abjad.annotate(note, 'foo', articulation)
            >>> abjad.inspect(note).get_annotation('foo')
            Articulation('accent', Up)

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
    def start_offset(self):
        r'''Gets start offset of indicator wrapper.

        This is either the wrapper's synthetic offset or the start offset of
        the wrapper's component.

        Returns offset.
        '''
        import abjad
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        return abjad.inspect(self._component).get_timespan().start_offset

    @property
    def synthetic_offset(self):
        r'''Gets synthetic offset of indicator wrapper.

        Synthetic offset is optional.

        Returns offset or none.
        '''
        return self._synthetic_offset
