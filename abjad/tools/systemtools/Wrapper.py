import copy
import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from .Tag import Tag


class Wrapper(AbjadValueObject):
    r"""
    Wrapper.

    ..  container:: example

        >>> component = abjad.Note("c'4")
        >>> articulation = abjad.Articulation('accent', direction=abjad.Up)
        >>> abjad.attach(articulation, component)
        >>> wrapper = abjad.inspect(component).wrapper()

        >>> abjad.f(wrapper)
        abjad.Wrapper(
            indicator=abjad.Articulation('accent', Up),
            tag=abjad.Tag(),
            )

    ..  container:: example

        Duplicate indicator warnings take two forms.

        >>> voice_1 = abjad.Voice("c''4 d'' e'' f''", name='VoiceI')
        >>> voice_2 = abjad.Voice("c'4 d' e' f'", name='VoiceII')
        >>> abjad.attach(abjad.Clef('alto'), voice_2[0])
        >>> staff = abjad.Staff([voice_1, voice_2], is_simultaneous=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            <<
                \context Voice = "VoiceI"
                {
                    c''4
                    d''4
                    e''4
                    f''4
                }
                \context Voice = "VoiceII"
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

        First form when attempting to attach a contexted indicator to a leaf
        that already carries a contexted indicator of the same type:

        >>> abjad.attach(abjad.Clef('treble'), voice_2[0])
        Traceback (most recent call last):
            ...
        abjad...PersistentIndicatorError: Can not attach ...
        <BLANKLINE>
            abjad.Clef('treble')
        <BLANKLINE>
            ... to Note("c'4") in VoiceII because ...
        <BLANKLINE>
        abjad.Wrapper(
            context='Staff',
            indicator=abjad.Clef('alto'),
            tag=abjad.Tag(),
            )
        <BLANKLINE>
            ... is already attached to the same leaf.
        <BLANKLINE>

        Second form when attempting to attach a contexted indicator to a leaf
        governed by some other component carrying a contexted indicator of the
        same type.

        >>> abjad.attach(abjad.Clef('treble'), voice_1[0])
        Traceback (most recent call last):
            ...
        abjad...PersistentIndicatorError: Can not attach ...
        <BLANKLINE>
            abjad.Clef('treble')
        <BLANKLINE>
            ... to Note("c''4") in VoiceI because ...
        <BLANKLINE>
        abjad.Wrapper(
            context='Staff',
            indicator=abjad.Clef('alto'),
            tag=abjad.Tag(),
            )
        <BLANKLINE>
            ... is already attached to Note("c'4") in VoiceII.
        <BLANKLINE>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_alternate',
        '_annotation',
        '_component',
        '_context',
        '_deactivate',
        '_effective_context',
        '_indicator',
        '_left_broken',
        '_right_broken',
        '_spanner',
        '_synthetic_offset',
        '_tag',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        alternate: typing.Tuple[str, str] = None,
        annotation: str = None,
        component=None,
        context: str = None,
        deactivate: bool = None,
        indicator=None,
        left_broken: bool = None,
        right_broken: bool = None,
        spanner=None,
        synthetic_offset: int = None,
        tag: typing.Union[str, Tag] = None,
        ) -> None:
        from abjad.tools.datastructuretools.Offset import Offset
        from abjad.tools.scoretools.Component import Component
        from abjad.tools.scoretools.Context import Context
        from abjad.tools.spannertools.Spanner import Spanner
        assert not isinstance(indicator, type(self)), repr(indicator)
        if alternate is not None:
            assert isinstance(alternate, tuple) and len(alternate) == 2
        self._alternate = alternate
        if annotation is not None:
            assert isinstance(annotation, str), repr(annotation)
        self._annotation = annotation
        if component is not None:
            assert isinstance(component, (Component, Spanner))
        self._component = component
        if deactivate is not None:
            deactivate = bool(deactivate)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if deactivate is not None:
            deactivate = bool(deactivate)
        self._deactivate = deactivate
        self._effective_context = None
        self._indicator = indicator
        if spanner is not None:
            assert isinstance(spanner, Spanner)
        self._spanner = spanner
        if left_broken is not None:
            left_broken = bool(left_broken)
        if left_broken and spanner is None:
            raise Exception('set left_broken only with spanners.')
        self._left_broken = left_broken
        if right_broken is not None:
            right_broken = bool(right_broken)
        if right_broken and spanner is None:
            raise Exception('set right_broken only with spanners.')
        self._right_broken = right_broken
        if synthetic_offset is not None:
            synthetic_offset = Offset(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if tag is not None:
            assert isinstance(tag, (str, Tag))
        tag = Tag(tag)
        self._tag: Tag = tag

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> 'Wrapper':
        r"""
        Copies indicator wrapper.

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

            Mutation preserves spanner:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, old_staff[:])
            >>> spanner.attach(abjad.Markup('pont.'), old_staff[0])
            >>> abjad.f(old_staff)
            \new Staff
            {
                c'4
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak dash-period 0
                - \tweak bound-details.left-broken.text ##f
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                indicator=abjad.Markup(
                    contents=['pont.'],
                    ),
                spanner=abjad.TextSpanner(),
                tag=abjad.Tag(),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff
            {
                c'4
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak dash-period 0
                - \tweak bound-details.left-broken.text ##f
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                indicator=abjad.Markup(
                    contents=['pont.'],
                    ),
                spanner=abjad.TextSpanner(),
                tag=abjad.Tag(),
                )

        ..  container:: example

            Preserves tag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> clef = abjad.Clef('alto')
            >>> abjad.attach(clef, old_staff[0], tag='RED:M1')
            >>> abjad.f(old_staff)
            \new Staff {
                \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

        ..  container:: example

            Preserves deactivate flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(
            ...     abjad.Clef('alto'),
            ...     old_staff[0],
            ...     deactivate=True,
            ...     tag='RED:M1',
            ...     )
            >>> abjad.f(old_staff)
            \new Staff {
                %@% \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                deactivate=True,
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                %@% \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                deactivate=True,
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

        ..  container:: example

            Preserves alternate tagging triple:

            >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> score = abjad.Score([staff])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> spanner = abjad.MetronomeMarkSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(
            ...     mark,
            ...     spanner[0],
            ...     alternate=('DarkRed', 'METRONOME_MARK_WITH_COLOR:M2'),
            ...     )
            >>> abjad.show(score) # doctest: +SKIP

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \time 3/8
                    c'8.
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #1
                        }
                %@% - \tweak bound-details.left.text \markup {     %! METRONOME_MARK_WITH_COLOR:M2
                %@%     \with-color                                %! METRONOME_MARK_WITH_COLOR:M2
                %@%         #(x11-color 'DarkRed)                  %! METRONOME_MARK_WITH_COLOR:M2
                %@%         {                                      %! METRONOME_MARK_WITH_COLOR:M2
                %@%             \fontsize                          %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 #-6                            %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 \general-align                 %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     #Y                         %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     #DOWN                      %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     \note-by-number            %! METRONOME_MARK_WITH_COLOR:M2
                %@%                         #2                     %! METRONOME_MARK_WITH_COLOR:M2
                %@%                         #0                     %! METRONOME_MARK_WITH_COLOR:M2
                %@%                         #1                     %! METRONOME_MARK_WITH_COLOR:M2
                %@%             \upright                           %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 {                              %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     =                          %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     60                         %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 }                              %! METRONOME_MARK_WITH_COLOR:M2
                %@%             \hspace                            %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 #1                             %! METRONOME_MARK_WITH_COLOR:M2
                %@%         }                                      %! METRONOME_MARK_WITH_COLOR:M2
                %@%     }                                          %! METRONOME_MARK_WITH_COLOR:M2
                    - \tweak dash-period 0
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 1
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.left-broken.text ##f
                    \startTextSpan
                    d'8.
                    e'4.
                    g'8.
                    f'8.
                    ef'4.
                    \stopTextSpan
                }
            >>

            >>> leaf = staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper(abjad.MetronomeMark)
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                alternate=('DarkRed', 'METRONOME_MARK_WITH_COLOR:M2'),
                context='Score',
                indicator=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                spanner=abjad.MetronomeMarkSpanner(
                    left_broken_text=False,
                    left_hspace=1,
                    parenthesize=False,
                    right_padding=1,
                    stem_height=1,
                    ),
                tag=abjad.Tag(),
                )


            >>> new_score = abjad.mutate(score).copy()
            >>> abjad.f(new_score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextSpanner.staff-padding = #3
                }
                {
                    \time 3/8
                    c'8.
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \fontsize
                            #-6
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            {
                                =
                                60
                            }
                        \hspace
                            #1
                        }
                %@% - \tweak bound-details.left.text \markup {     %! METRONOME_MARK_WITH_COLOR:M2
                %@%     \with-color                                %! METRONOME_MARK_WITH_COLOR:M2
                %@%         #(x11-color 'DarkRed)                  %! METRONOME_MARK_WITH_COLOR:M2
                %@%         {                                      %! METRONOME_MARK_WITH_COLOR:M2
                %@%             \fontsize                          %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 #-6                            %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 \general-align                 %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     #Y                         %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     #DOWN                      %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     \note-by-number            %! METRONOME_MARK_WITH_COLOR:M2
                %@%                         #2                     %! METRONOME_MARK_WITH_COLOR:M2
                %@%                         #0                     %! METRONOME_MARK_WITH_COLOR:M2
                %@%                         #1                     %! METRONOME_MARK_WITH_COLOR:M2
                %@%             \upright                           %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 {                              %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     =                          %! METRONOME_MARK_WITH_COLOR:M2
                %@%                     60                         %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 }                              %! METRONOME_MARK_WITH_COLOR:M2
                %@%             \hspace                            %! METRONOME_MARK_WITH_COLOR:M2
                %@%                 #1                             %! METRONOME_MARK_WITH_COLOR:M2
                %@%         }                                      %! METRONOME_MARK_WITH_COLOR:M2
                %@%     }                                          %! METRONOME_MARK_WITH_COLOR:M2
                    - \tweak dash-period 0
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 1
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.left-broken.text ##f
                    \startTextSpan
                    d'8.
                    e'4.
                    g'8.
                    f'8.
                    ef'4.
                    \stopTextSpan
                }
            >>

            >>> leaf = abjad.inspect(new_score).get_leaf(0)
            >>> wrapper = abjad.inspect(leaf).wrapper(abjad.MetronomeMark)
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                alternate=('DarkRed', 'METRONOME_MARK_WITH_COLOR:M2'),
                context='Score',
                indicator=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                spanner=abjad.MetronomeMarkSpanner(
                    left_broken_text=False,
                    left_hspace=1,
                    parenthesize=False,
                    right_padding=1,
                    stem_height=1,
                    ),
                tag=abjad.Tag(),
                )

        Copies all properties except component and spanner.
        
        Copy operations must supply component and spanner after wrapper copy.

        Returns new indicator wrapper.
        """
        new = type(self)(
            alternate=self.alternate,
            annotation=self.annotation,
            component=None,
            context=self.context,
            deactivate=self.deactivate,
            indicator=copy.copy(self.indicator),
            spanner = None,
            synthetic_offset=self.synthetic_offset,
            tag=self.tag,
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
        component._wrappers.append(self)

    def _detach(self):
        self._unbind_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
        import abjad
        if self.context is None:
            return None
        context = getattr(abjad, self.context, self.context)
        if isinstance(context, type):
            for component in abjad.inspect(self.component).get_parentage():
                if not isinstance(component, abjad.Context):
                    continue
                if isinstance(component, context):
                    return component
        elif isinstance(context, str):
            for component in abjad.inspect(self.component).get_parentage():
                if not isinstance(component, abjad.Context):
                    continue
                if (component.name == context or
                    component.lilypond_type == context):
                    return component
        else:
            raise TypeError('must be context or string: {context!r}.')

    def _get_effective_context(self):
        if self.component is not None:
            self.component._update_now(indicators=True)
        return self._effective_context

    def _get_format_pieces(self):
        import abjad
        result = []
        if self.annotation:
            return result
        if hasattr(self.indicator, '_get_lilypond_format_bundle'):
            bundle = self.indicator._get_lilypond_format_bundle(self.component)
            bundle.tag_format_contributions(
                self.tag,
                deactivate=self.deactivate,
                )
            return bundle
        try:
            context = self._get_effective_context()
            lilypond_format = self.indicator._get_lilypond_format(
                context=context,
                )
        except TypeError:
            lilypond_format = self.indicator._get_lilypond_format()
        if isinstance(lilypond_format, str):
            lilypond_format = [lilypond_format]
        assert isinstance(lilypond_format, (tuple, list))
        lilypond_format = abjad.LilyPondFormatManager.tag(
            lilypond_format,
            self.tag,
            deactivate=self.deactivate,
            )
        result.extend(lilypond_format)
        if self._get_effective_context() is not None:
            return result
        if isinstance(self.indicator, abjad.TimeSignature):
            if isinstance(self.component, abjad.Measure):
                return result
        result = [rf'%%% {_} %%%' for _ in result]
        return result

    def _get_format_specification(self):
        import abjad
        keywords = [
            'alternate',
            'annotation',
            'context',
            'deactivate',
            'indicator',
            'left_broken',
            'right_broken',
            'spanner',
            'synthetic_offset',
            'tag',
            ]
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=None,
            storage_format_kwargs_names=keywords,
            )

    def _is_formattable_for_component(self, component):
        import abjad
        if self.annotation:
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
            if hasattr(component, '_wrappers'):
                if self in component._wrappers:
                    component._wrappers.remove(self)
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
        current_effective_context = self._effective_context
        correct_effective_context = self._find_correct_effective_context()
        if current_effective_context is not correct_effective_context:
            self._bind_correct_effective_context(correct_effective_context)

    def _warn_duplicate_indicator(self, component):
        import abjad
        if isinstance(component, abjad.Spanner):
            return
        if isinstance(self.indicator, abjad.LilyPondLiteral):
            return
        if self.deactivate is True:
            return
        prototype = type(self.indicator)
        wrapper = abjad.inspect(component).effective_wrapper(prototype)
        if (wrapper is not None and
            wrapper.context is not None and
            wrapper.deactivate is not True and
            wrapper.indicator != self.indicator):
            if wrapper.start_offset == self.start_offset:
                parentage = abjad.inspect(component).get_parentage()
                context = parentage.get_first(abjad.Context)
                message = f'\n\nCan not attach ...\n\n{self.indicator}\n\n...'
                message += f' to {repr(component)}'
                message += f' in {context.name} because ...'
                message += f'\n\n{format(wrapper)}\n\n'
                message += '... is already attached'
                if component is wrapper.component:
                    message += ' to the same leaf.'
                else:
                    inspection = abjad.inspect(wrapper.component)
                    parentage = inspection.get_parentage()
                    context = parentage.get_first(abjad.Context)
                    message += f' to {repr(wrapper.component)}'
                    message += f' in {context.name}.'
                message += '\n'
                message = message.format(
                    self.indicator,
                    repr(component),
                    format(wrapper),
                    repr(wrapper.component),
                    )
                raise abjad.PersistentIndicatorError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def alternate(self) -> typing.Optional[typing.Tuple[str, str]]:
        """
        Gets alternate tagging information.

        Set only by ``MetronomeMarkSpanner.attach(..., alternate=None)``
        keyword.

        Returns (color, tag) pair, or none.
        """
        return self._alternate

    @property
    def annotation(self) -> typing.Optional[str]:
        """
        Gets indicator wrapper annotation.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', direction=abjad.Up)
            >>> abjad.attach(articulation, note)
            >>> wrapper = abjad.inspect(note).wrapper()
            >>> wrapper.annotation is None
            True

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', direction=abjad.Up)
            >>> abjad.annotate(note, 'foo', articulation)
            >>> abjad.inspect(note).get_annotation('foo')
            Articulation('accent', Up)

        """
        return self._annotation

    @property
    def component(self):
        """
        Gets start component of indicator wrapper.

        Returns component.
        """
        from abjad.tools.spannertools.Spanner import Spanner
        if isinstance(self._component, Spanner):
            if self._component:
                return self._component[0]
            else:
                return None
        return self._component

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context of indicator wrapper.
        """
        return self._context

    @property
    def deactivate(self) -> typing.Optional[bool]:
        """
        Is true when wrapper deactivates tag.
        """
        assert self._deactivate in (True, False, None)
        return self._deactivate

    @deactivate.setter
    def deactivate(self, argument):
        assert argument in (True, False, None)
        self._deactivate: typing.Optional[bool] = argument

    @property
    def indicator(self) -> typing.Any:
        """
        Gets indicator of indicator wrapper.
        """
        return self._indicator

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is left-open.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is right-open.
        """
        return self._right_broken

    @property
    def spanner(self):
        """
        Gets wrapper spanner.

        Returns spanner or none.
        """
        return self._spanner

    @property
    def start_offset(self):
        """
        Gets start offset of indicator wrapper.

        This is either the wrapper's synthetic offset or the start offset of
        the wrapper's component.

        Returns offset.
        """
        from abjad.tools.topleveltools.inspect import inspect
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        return inspect(self._component).get_timespan().start_offset

    @property
    def synthetic_offset(self):
        """
        Gets synthetic offset of indicator wrapper.

        Returns offset or none.
        """
        return self._synthetic_offset

    @property
    def tag(self) -> Tag:
        """
        Gets and sets tag.
        """
        assert isinstance(self._tag, Tag), repr(self._tag)
        return self._tag

    @tag.setter
    def tag(self, argument):
        if not isinstance(argument, (str, Tag)):
            raise Exception(f'string or tag: {argument!r}.')
        tag = Tag(argument)
        self._tag = tag
