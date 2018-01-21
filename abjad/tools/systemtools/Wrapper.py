import copy
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Wrapper(AbjadValueObject):
    r'''Wrapper.

    ..  container:: example

        >>> component = abjad.Note("c'4")
        >>> articulation = abjad.Articulation('accent', abjad.Up)
        >>> abjad.attach(articulation, component)
        >>> wrapper = abjad.inspect(component).wrapper()

        >>> abjad.f(wrapper)
        abjad.Wrapper(
            component=abjad.Note("c'4 ^\\accent"),
            indicator=abjad.Articulation('accent', Up),
            )

    '''

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
        '_left_open',
        '_right_open',
        '_site',
        '_spanner',
        '_synthetic_offset',
        '_tag',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        alternate=None,
        annotation=None,
        component=None,
        context=None,
        deactivate=None,
        indicator=None,
        left_open=None,
        right_open=None,
        site=None,
        spanner=None,
        synthetic_offset=None,
        tag=None,
        ):
        import abjad
        assert not isinstance(indicator, type(self)), repr(indicator)
        if alternate is not None:
            assert isinstance(alternate, tuple) and len(alternate) == 3
        self._alternate = alternate
        if annotation is not None:
            assert isinstance(annotation, str), repr(annotation)
        self._annotation = annotation
        if component is not None:
            prototype = (abjad.Component, abjad.Spanner)
            assert isinstance(component, prototype)
        self._component = component
        if deactivate is not None:
            deactivate = bool(deactivate)
        if context is not None:
            if isinstance(context, type):
                assert issubclass(context, abjad.Context)
            else:
                prototype = (abjad.Context, str)
                assert isinstance(context, prototype), repr(context)
        self._context = context
        self._deactivate = deactivate
        self._effective_context = None
        self._indicator = indicator
        if spanner is not None:
            assert isinstance(spanner, abjad.Spanner)
        self._spanner = spanner
        if left_open is not None:
            left_open = bool(left_open)
        if left_open and spanner is None:
            raise Exception('set open left only with spanners.')
        self._left_open = left_open
        if right_open is not None:
            right_open = bool(right_open)
        if right_open and spanner is None:
            raise Exception('set open right only with spanners.')
        self._right_open = right_open
        if site is not None:
            assert isinstance(site, str), repr(site)
        self._site = site
        if synthetic_offset is not None:
            synthetic_offset = abjad.Offset(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if isinstance(tag, abjad.Enumeration):
            tag = tag.name
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag

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

            Mutation preserves spanner:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, old_staff[:])
            >>> spanner.attach(abjad.Markup('pont.'), old_staff[0])
            >>> abjad.f(old_staff)
            \new Staff {
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            pont.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-period = 0
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                component=abjad.Note("\\once \\override TextSpanner.Y-extent = ##f\n\\once \\override TextSpanner.bound-details.left-broken.text = ##f\n\\once \\override TextSpanner.bound-details.left.stencil-align-dir-y = #center\n\\once \\override TextSpanner.bound-details.left.text = \\markup {\n    \\concat\n        {\n            pont.\n            \\hspace\n                #0.25\n        }\n    }\n\\once \\override TextSpanner.bound-details.right-broken.padding = 0\n\\once \\override TextSpanner.bound-details.right-broken.text = ##f\n\\once \\override TextSpanner.bound-details.right.padding = 1.5\n\\once \\override TextSpanner.bound-details.right.stencil-align-dir-y = #center\n\\once \\override TextSpanner.dash-period = 0\nc'4 \\startTextSpan"),
                indicator=abjad.Markup(
                    contents=['pont.'],
                    ),
                spanner=abjad.TextSpanner(),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            pont.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-period = 0
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                component=abjad.Note("\\once \\override TextSpanner.Y-extent = ##f\n\\once \\override TextSpanner.bound-details.left-broken.text = ##f\n\\once \\override TextSpanner.bound-details.left.stencil-align-dir-y = #center\n\\once \\override TextSpanner.bound-details.left.text = \\markup {\n    \\concat\n        {\n            pont.\n            \\hspace\n                #0.25\n        }\n    }\n\\once \\override TextSpanner.bound-details.right-broken.padding = 0\n\\once \\override TextSpanner.bound-details.right-broken.text = ##f\n\\once \\override TextSpanner.bound-details.right.padding = 1.5\n\\once \\override TextSpanner.bound-details.right.stencil-align-dir-y = #center\n\\once \\override TextSpanner.dash-period = 0\nc'4 \\startTextSpan"),
                indicator=abjad.Markup(
                    contents=['pont.'],
                    ),
                spanner=abjad.TextSpanner(),
                )

        ..  container:: example

            Preserves tag and site:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> clef = abjad.Clef('alto')
            >>> abjad.attach(clef, old_staff[0], site='M1', tag='RED')
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
                component=abjad.Note('\\clef "alto" %! RED:M1\nc\'4'),
                context='Staff',
                indicator=abjad.Clef('alto'),
                site='M1',
                tag='RED',
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
                component=abjad.Note('\\clef "alto" %! RED:M1\nc\'4'),
                context='Staff',
                indicator=abjad.Clef('alto'),
                site='M1',
                tag='RED',
                )

        ..  container:: example

            Preserves deactivate flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(
            ...     abjad.Clef('alto'),
            ...     old_staff[0],
            ...     deactivate=True,
            ...     site='M1',
            ...     tag='RED',
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
                component=abjad.Note('%@% \\clef "alto" %! RED:M1\nc\'4'),
                context='Staff',
                deactivate=True,
                indicator=abjad.Clef('alto'),
                site='M1',
                tag='RED',
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
                component=abjad.Note('%@% \\clef "alto" %! RED:M1\nc\'4'),
                context='Staff',
                deactivate=True,
                indicator=abjad.Clef('alto'),
                site='M1',
                tag='RED',
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
            ...     alternate=('DarkRed', 'M2', 'METRONOME_MARK_WITH_COLOR'),
            ...     )
            >>> abjad.show(score) # doctest: +SKIP

            >>> abjad.f(score)
            \new Score <<
                \new Staff \with {
                    \override TextSpanner.staff-padding = #3
                } {
                    %@% \once \override TextSpanner.bound-details.left.text = %! METRONOME_MARK_WITH_COLOR:M2
                    %@% \markup {                                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%     \with-color                                       %! METRONOME_MARK_WITH_COLOR:M2
                    %@%         #(x11-color 'DarkRed)                         %! METRONOME_MARK_WITH_COLOR:M2
                    %@%         {                                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%             \fontsize                                 %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 #-6                                   %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 \general-align                        %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     #Y                                %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     #DOWN                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     \note-by-number                   %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                         #2                            %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                         #0                            %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                         #1                            %! METRONOME_MARK_WITH_COLOR:M2
                    %@%             \upright                                  %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 {                                     %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     =                                 %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     60                                %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 }                                     %! METRONOME_MARK_WITH_COLOR:M2
                    %@%             \hspace                                   %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 #1                                    %! METRONOME_MARK_WITH_COLOR:M2
                    %@%         }                                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%     }                                                 %! METRONOME_MARK_WITH_COLOR:M2
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    e'4.
                    g'8.
                    f'8.
                    ef'4. \stopTextSpan
                }
            >>

            >>> leaf = staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper(abjad.MetronomeMark)
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                alternate=('DarkRed', 'M2', 'METRONOME_MARK_WITH_COLOR'),
                component=abjad.Note(...),
                context='Score',
                indicator=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                spanner=abjad.MetronomeMarkSpanner(
                    left_hspace=1,
                    parenthesize=False,
                    right_padding=1,
                    stem_height=1,
                    ),
                )


            >>> new_score = abjad.mutate(score).copy()
            >>> abjad.f(new_score)
            \new Score <<
                \new Staff \with {
                    \override TextSpanner.staff-padding = #3
                } {
                    %@% \once \override TextSpanner.bound-details.left.text = %! METRONOME_MARK_WITH_COLOR:M2
                    %@% \markup {                                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%     \with-color                                       %! METRONOME_MARK_WITH_COLOR:M2
                    %@%         #(x11-color 'DarkRed)                         %! METRONOME_MARK_WITH_COLOR:M2
                    %@%         {                                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%             \fontsize                                 %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 #-6                                   %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 \general-align                        %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     #Y                                %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     #DOWN                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     \note-by-number                   %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                         #2                            %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                         #0                            %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                         #1                            %! METRONOME_MARK_WITH_COLOR:M2
                    %@%             \upright                                  %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 {                                     %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     =                                 %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                     60                                %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 }                                     %! METRONOME_MARK_WITH_COLOR:M2
                    %@%             \hspace                                   %! METRONOME_MARK_WITH_COLOR:M2
                    %@%                 #1                                    %! METRONOME_MARK_WITH_COLOR:M2
                    %@%         }                                             %! METRONOME_MARK_WITH_COLOR:M2
                    %@%     }                                                 %! METRONOME_MARK_WITH_COLOR:M2
                    \once \override TextSpanner.Y-extent = ##f
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text =
                    \markup {
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
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.padding = 1
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-period = 0
                    \time 3/8
                    c'8. \startTextSpan
                    d'8.
                    e'4.
                    g'8.
                    f'8.
                    ef'4. \stopTextSpan
                }
            >>

            >>> leaf = abjad.inspect(new_score).get_leaf(0)
            >>> wrapper = abjad.inspect(leaf).wrapper(abjad.MetronomeMark)
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                alternate=('DarkRed', 'M2', 'METRONOME_MARK_WITH_COLOR'),
                component=abjad.Note(...),
                context='Score',
                indicator=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                spanner=abjad.MetronomeMarkSpanner(
                    left_hspace=1,
                    parenthesize=False,
                    right_padding=1,
                    stem_height=1,
                    ),
                )

        Copies all properties except component and spanner.
        
        Copy operations must supply component and spanner after wrapper copy.

        Returns new indicator wrapper.
        '''
        new = type(self)(
            alternate=self.alternate,
            annotation=self.annotation,
            component=None,
            context=self.context,
            deactivate=self.deactivate,
            indicator=copy.copy(self.indicator),
            site=self.site,
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
            message = 'must be context or string: {!r}.'
            message = message.format(context)
            raise TypeError(message)

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
                site=self.site,
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
            site=self.site,
            )
        result.extend(lilypond_format)
        if self._get_effective_context() is not None:
            return result
        if isinstance(self.indicator, abjad.TimeSignature):
            if isinstance(self.component, abjad.Measure):
                return result
        result = [r'%%% {} %%%'.format(_) for _ in result]
        return result

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
        prototype = type(self.indicator)
        wrapper = abjad.inspect(component).effective_wrapper(prototype)
        if (wrapper is not None and
            wrapper.context is not None and
            wrapper.indicator != self.indicator):
            if wrapper.start_offset == self.start_offset:
                message = 'Can not attach ...\n\n{}\n\n...to ...\n\n{}'
                message += '\n\n... because ...\n\n{}\n\n'
                message += '... is already attached to ...\n\n'
                message += '{}\n\nSee:\n\n{}'
                message = message.format(
                    self.indicator,
                    component,
                    wrapper.indicator,
                    wrapper.component,
                    format(wrapper),
                    )
                raise Exception(message)

    ### PUBLIC PROPERTIES ###

    @property
    def alternate(self):
        r'''Gets alternate tagging information.

        Set only by ``MetronomeMarkSpanner.attach(..., alternate=None)``
        keyword.

        Returns (color, site, tag) triple, or none.
        '''
        return self._alternate

    @property
    def annotation(self):
        r'''Gets indicator wrapper annotation.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', abjad.Up)
            >>> abjad.attach(articulation, note)
            >>> wrapper = abjad.inspect(note).wrapper()
            >>> wrapper.annotation is None
            True

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', abjad.Up)
            >>> abjad.annotate(note, 'foo', articulation)
            >>> abjad.inspect(note).get_annotation('foo')
            Articulation('accent', Up)

        Returns string or none.
        '''
        return self._annotation

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
    def deactivate(self):
        r'''Is true when wrapper deactivates tag.

        Returns true, false or none.
        '''
        return self._deactivate

    @property
    def indicator(self):
        r'''Gets indicator of indicator wrapper.

        Returns indicator.
        '''
        return self._indicator

    @property
    def left_open(self):
        r'''Is true when spanner is left-open.

        Defaults to none.

        Set to true, false or none.
        '''
        return self._left_open

    @property
    def site(self):
        r'''Gets site.

        Site is optional.

        Returns string or none.
        '''
        return self._site

    @property
    def right_open(self):
        r'''Is true when spanner is right-open.

        Defaults to none.

        Set to true, false or none.
        '''
        return self._right_open

    @property
    def spanner(self):
        r'''Gets wrapper spanner.

        Returns spanner or none.
        '''
        return self._spanner

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

    @property
    def tag(self):
        r'''Gets tag.

        Tag is optional.

        Returns string or none.
        '''
        return self._tag
