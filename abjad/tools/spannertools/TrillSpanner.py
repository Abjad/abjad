from .Spanner import Spanner


class TrillSpanner(Spanner):
    r'''Trill spanner.

    ..  container:: example

        Attaches unpitched trill spanner to all notes in staff:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> trill = abjad.TrillSpanner()
        >>> abjad.attach(trill, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \startTrillSpan
                d'8
                e'8
                f'8 \stopTrillSpan
            }

    ..  container:: example

        Attaches pitched trill spanner to all notes in staff:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> trill = abjad.TrillSpanner(pitch=abjad.NamedPitch("cs'"))
        >>> abjad.attach(trill, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \pitchedTrill
                c'8
                \startTrillSpan cs'
                d'8
                e'8
                f'8 \stopTrillSpan
            }

    ..  container:: example

        Requires at least two leaves:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> trill = abjad.TrillSpanner()
        >>> abjad.attach(trill, staff[:1])

    ..  container:: example

        REGRESSION. Pitched trill spanner must appear after markup to avoid
        hiding markup in graphic output:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up)
        >>> abjad.attach(markup, staff[0])
        >>> trill_spanner = abjad.TrillSpanner(pitch='Db4')
        >>> abjad.attach(trill_spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=True)
            \new Staff
            {
                \pitchedTrill
                c'4
                ^ \markup { Allegro }
                \startTrillSpan df'
                d'4
                e'4
                r4
                \stopTrillSpan
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_interval',
        '_is_harmonic',
        '_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        interval=None,
        is_harmonic=None,
        overrides=None,
        pitch=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        if interval is not None and pitch is not None:
            message = 'only pitch or interval, not both: {!r} + {!r}.'
            message = message.format(interval, pitch)
            raise Exception(message)
        self._interval = interval
        if is_harmonic is not None:
            is_harmonic = bool(is_harmonic)
        self._is_harmonic = is_harmonic
        if pitch is not None:
            pitch = abjad.NamedPitch(pitch)
        self._pitch = pitch

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        self._is_harmonic = self.is_harmonic
        new._pitch = self.pitch

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        if len(self) == 1 and self._left_broken:
            strings = [r'\stopTrillSpan']
            strings = self._tag_show(strings)
            bundle.right.spanner_stops.extend(strings)
            return bundle
        if leaf is self[0]:
            strings = abjad.override(self)._list_format_contributions(
                'override',
                once=False,
                )
            if self._left_broken:
                strings = self._tag_hide(strings)
            bundle.grob_overrides.extend(strings)
            if self.pitch is not None:
                pitch_string = str(self.pitch)
            elif self.interval is not None:
                pitch = leaf.written_pitch + self.interval
                pitch_string = str(pitch)
            else:
                pitch_string = None
            string = r'\startTrillSpan'
            if pitch_string:
                string += ' ' + pitch_string
            strings = [string]
            if self._left_broken:
                strings = self._tag_hide(strings)
            # important: pitch trill must start AFTER markup
            bundle.after.spanner_starts.extend(strings)
            if self.pitch is not None or self.interval is not None:
                strings = [r'\pitchedTrill']
                if self._left_broken:
                    strings = self._tag_hide(strings)
                bundle.opening.spanners.extend(strings)
                if self.is_harmonic:
                    string = '(lambda (grob) (grob-interpret-markup grob'
                    string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
                    scheme = abjad.Scheme(string, verbatim=True)
                    # TODO: use strings instead of override interface:
                    abjad.override(leaf).trill_pitch_head.stencil = scheme
        if leaf is self[-1]:
            manager = abjad.override(self)
            strings = manager._list_format_contributions('revert')
            if self._right_broken:
                strings = self._tag_hide(strings)
            bundle.grob_reverts.extend(strings)
            if 1 < len(self):
                strings = [r'\stopTrillSpan']
                if self._right_broken:
                    strings = self._tag_hide(strings)
                bundle.right.spanner_stops.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    def cross_segment_examples(self):
        r'''Cross-segment examples.

        ..  container:: example

            Cross-segment example #1 (one-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_1[-1:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \startTrillSpan
                }

            >>> segment_2 = abjad.Voice("g'4 f'2 r4", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_2[:1], left_broken=True)
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                %@% \stopTrillSpan                                %! SHOW_TO_JOIN_BROKEN_SPANNERS
                    f'2
                    r4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file, strict=50) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \startTrillSpan
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                        \stopTrillSpan                            %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        f'2
                        r4
                    }
                }

        ..  container:: example

            Cross-segment example #2 (one-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_1[-1:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \startTrillSpan
                }

            >>> segment_2 = abjad.Voice("g'4 f'2 r4", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_2[:], left_broken=True)
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                    \startTrillSpan                               %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    f'2
                    r4
                    \stopTrillSpan
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file, strict=50) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \startTrillSpan
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                    %%% \startTrillSpan                           %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        f'2
                        r4
                        \stopTrillSpan
                    }
                }

        ..  container:: example

            Cross-segment example #3 (many-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_1[:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \startTrillSpan
                    d'4
                    e'4
                    f'4
                    \stopTrillSpan                                %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("g'4 f'2 r4", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_2[:1], left_broken=True)
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                %@% \stopTrillSpan                                %! SHOW_TO_JOIN_BROKEN_SPANNERS
                    f'2
                    r4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file, strict=50) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \startTrillSpan
                        d'4
                        e'4
                        f'4
                    %%% \stopTrillSpan                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                        \stopTrillSpan                            %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        f'2
                        r4
                    }
                }

        ..  container:: example

            Cross-segment example #4 (many-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_1[:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \startTrillSpan
                    d'4
                    e'4
                    f'4
                    \stopTrillSpan                                %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("g'4 f'2 r4", name='MainVoice')
            >>> abjad.attach(abjad.TrillSpanner(), segment_2[:], left_broken=True)
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                    \startTrillSpan                               %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    f'2
                    r4
                    \stopTrillSpan
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file, strict=50) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \startTrillSpan
                        d'4
                        e'4
                        f'4
                    %%% \stopTrillSpan                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                    %%% \startTrillSpan                           %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        f'2
                        r4
                        \stopTrillSpan
                    }
                }

        '''
        pass

    @property
    def interval(self):
        r'''Gets interval of trill.

        ..  container:: example

            Attaches semitone trill:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner(
            ...     interval=abjad.NamedInterval('m2'),
            ...     )
            >>> abjad.attach(trill, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \pitchedTrill
                    c'8
                    \startTrillSpan df'
                    d'8
                    e'8
                    f'8 \stopTrillSpan
                }

        ..  container:: example

            Attaches whole tone trill:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner(
            ...     interval=abjad.NamedInterval('M2'),
            ...     )
            >>> abjad.attach(trill, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \pitchedTrill
                    c'8
                    \startTrillSpan d'
                    d'8
                    e'8
                    f'8 \stopTrillSpan
                }

        Defaults to none.

        Set to interval or none.

        Returns interval or none.
        '''
        return self._interval

    @property
    def is_harmonic(self):
        r'''Is true when trill pitch note-head should print as a white diamond.
        Otherwise false.

        ..  container:: example

            Attaches harmonic trill:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner(
            ...     is_harmonic=True,
            ...     pitch=abjad.NamedPitch("d'"),
            ...     )
            >>> abjad.attach(trill, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \once \override TrillPitchHead.stencil = #(lambda (grob) (grob-interpret-markup grob #{ \markup \musicglyph #"noteheads.s0harmonic" #}))
                    \pitchedTrill
                    c'8
                    \startTrillSpan d'
                    d'8
                    e'8
                    f'8 \stopTrillSpan
                }

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._is_harmonic

    @property
    def pitch(self):
        r'''Gets optional pitch of trill spanner.

        ..  container:: example

            Returns pitch when trill spanner is pitched:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> pitch = abjad.NamedPitch('C#4')
            >>> trill = abjad.TrillSpanner(pitch=pitch)
            >>> abjad.attach(trill, staff[:2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \pitchedTrill
                    c'8
                    \startTrillSpan cs'
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            >>> trill.pitch
            NamedPitch("cs'")

        ..  container:: example

            Returns none when trill spanner is unpitched:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner()
            >>> abjad.attach(trill, staff[:2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \startTrillSpan
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            >>> trill.pitch is None
            True

        Formats LilyPond ``\pitchedTrill`` command on first leaf in spanner.

        Defaults to none.

        Set to named pitch or none.

        Returns named pitch or none.
        '''
        return self._pitch

    @property
    def written_pitch(self):
        r'''Gets written pitch of trill spanner.

        ..  container:: example

            Returns pitch when trill spanner is pitched:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> pitch = abjad.NamedPitch('C#4')
            >>> trill = abjad.TrillSpanner(pitch=pitch)
            >>> abjad.attach(trill, staff[:2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \pitchedTrill
                    c'8
                    \startTrillSpan cs'
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            >>> trill.written_pitch
            NamedPitch("cs'")

        ..  container:: example

            Returns none when trill spanner is unpitched:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner()
            >>> abjad.attach(trill, staff[:2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \startTrillSpan
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            >>> trill.written_pitch is None
            True

        Alias defined equal to `pitch` of trill spanner.

        Defaults to none.

        Property can not be set.

        Returns named pitch or none.
        '''
        return self.pitch
