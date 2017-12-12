from .Spanner import Spanner


class ComplexTrillSpanner(Spanner):
    r'''Complex trill spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 ~ c'8 d'8 r8 e'8 ~ e'8 r8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4 ~
                c'8
                d'8
                r8
                e'8 ~
                e'8
                r8
            }

        >>> complex_trill = abjad.ComplexTrillSpanner(
        ...     interval='P4',
        ...     )
        >>> abjad.attach(complex_trill, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \pitchedTrill
                c'4 ~ \startTrillSpan f'
                c'8
                <> \stopTrillSpan
                \once \override TrillSpanner.bound-details.left.text = \markup {
                    \null
                    }
                \pitchedTrill
                d'8 \startTrillSpan g'
                <> \stopTrillSpan
                r8
                \pitchedTrill
                e'8 ~ \startTrillSpan a'
                e'8
                <> \stopTrillSpan
                r8
            }

    Allows for specifying a trill pitch via a named interval.

    Avoids silences.

    Restarts the trill on every new pitched logical tie.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_interval',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        interval=None,
        overrides=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        if interval is not None:
            interval = abjad.NamedInterval(interval)
        self._interval = interval

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._interval = self.interval

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (
            abjad.Rest,
            abjad.MultimeasureRest,
            abjad.Skip,
            )
        if isinstance(leaf, prototype):
            return bundle
        logical_tie = abjad.inspect(leaf).get_logical_tie()
        if leaf is logical_tie.head:
            previous_leaf = leaf._get_leaf(-1)
            if (previous_leaf is not None and
                not isinstance(previous_leaf, prototype) and
                abjad.inspect(previous_leaf).get_spanners(type(self))):
                grob_override = abjad.LilyPondGrobOverride(
                    grob_name='TrillSpanner',
                    once=True,
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=abjad.Markup(r'\null'),
                    )
                string = grob_override.override_string
                bundle.grob_overrides.append(string)
            if self.interval is not None:
                string = r'\pitchedTrill'
                bundle.opening.spanners.append(string)
                if isinstance(leaf, abjad.Note):
                    written_pitch = leaf.written_pitch
                elif isinstance(leaf, abjad.Chord):
                    if 0 < self.interval.semitones:
                        written_pitch = max(leaf.written_pitches)
                    elif self.interval.semitones < 0:
                        written_pitch = min(leaf.written_pitches)
                trill_pitch = written_pitch.transpose(self.interval)
                string = r'\startTrillSpan {!s}'.format(trill_pitch)
            else:
                string = r'\startTrillSpan'
            bundle.right.trill_pitches.append(string)
        if leaf is logical_tie.tail:
            next_leaf = leaf._get_leaf(1)
            if next_leaf is not None:
                string = r'<> \stopTrillSpan'
                bundle.after.commands.append(string)
            else:
                string = r'\stopTrillSpan'
                bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def interval(self):
        r'''Gets optional interval of trill spanner.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> interval = abjad.NamedInterval('m3')
            >>> complex_trill = abjad.ComplexTrillSpanner(interval=interval)
            >>> abjad.attach(complex_trill, staff[1:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'4
                    \pitchedTrill
                    d'4 \startTrillSpan f'
                    <> \stopTrillSpan
                    \once \override TrillSpanner.bound-details.left.text = \markup {
                        \null
                        }
                    \pitchedTrill
                    e'4 \startTrillSpan g'
                    <> \stopTrillSpan
                    f'4
                }

            >>> complex_trill.interval
            NamedInterval('+m3')

        '''
        return self._interval
