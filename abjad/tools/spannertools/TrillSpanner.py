# -*- coding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class TrillSpanner(Spanner):
    r'''Trill spanner.

    ::

        >>> import abjad

    ..  container:: example

        Attaches unpitched trill spanner to all notes in staff:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner()
            >>> abjad.attach(trill, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'8 \startTrillSpan
                d'8
                e'8
                f'8 \stopTrillSpan
            }

    ..  container:: example

        Attaches pitched trill spanner to all notes in staff:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> trill = abjad.TrillSpanner(pitch=abjad.NamedPitch("cs'"))
            >>> abjad.attach(trill, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \pitchedTrill
                c'8 \startTrillSpan cs'
                d'8
                e'8
                f'8 \stopTrillSpan
            }

    ..  container:: example

        Requires at least two leaves:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> trill = abjad.TrillSpanner()
            >>> abjad.attach(trill, staff[:1])
            Traceback (most recent call last):
                ...
            Exception: TrillSpanner() attachment test fails for Selection([Note("c'4")]).

    Formats LilyPond ``\startTrillSpan`` on first leaf in spanner.

    Formats LilyPond ``\stopTrillSpan`` on last leaf in spanner.
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
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        self._interval = interval
        if is_harmonic is not None:
            is_harmonic = bool(is_harmonic)
        self._is_harmonic = is_harmonic
        if pitch is not None:
            pitch = pitchtools.NamedPitch(pitch)
        self._pitch = pitch

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        return self._at_least_two_leaves(argument)

    def _copy_keyword_args(self, new):
        self._is_harmonic = self.is_harmonic
        new._pitch = self.pitch

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        if self._is_my_first_leaf(leaf):
            contributions = abjad.override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            bundle.grob_overrides.extend(contributions)
            string = r'\startTrillSpan'
            bundle.right.spanner_starts.append(string)
            if self.pitch is not None or self.interval is not None:
                string = r'\pitchedTrill'
                bundle.opening.spanners.append(string)
                if self.pitch is not None:
                    string = str(self.pitch)
                    bundle.right.trill_pitches.append(string)
                elif self.interval is not None:
                    pitch = leaf.written_pitch + self.interval
                    string = str(pitch)
                    bundle.right.trill_pitches.append(string)
                if self.is_harmonic:
                    string = '(lambda (grob) (grob-interpret-markup grob'
                    string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
                    scheme = abjad.Scheme(string, verbatim=True)
                    abjad.override(leaf).trill_pitch_head.stencil = scheme
        if self._is_my_last_leaf(leaf):
            manager = abjad.override(self)
            contributions = manager._list_format_contributions('revert')
            bundle.grob_reverts.extend(contributions)
            string = r'\stopTrillSpan'
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def interval(self):
        r'''Gets interval of trill.

        ..  container:: example

            Attaches semitone trill:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> trill = abjad.TrillSpanner(
                ...     interval=abjad.NamedInterval('m2'),
                ...     )
                >>> abjad.attach(trill, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \pitchedTrill
                    c'8 \startTrillSpan df'
                    d'8
                    e'8
                    f'8 \stopTrillSpan
                }

        ..  container:: example

            Attaches whole tone trill:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> trill = abjad.TrillSpanner(
                ...     interval=abjad.NamedInterval('M2'),
                ...     )
                >>> abjad.attach(trill, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \pitchedTrill
                    c'8 \startTrillSpan d'
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

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> trill = abjad.TrillSpanner(
                ...     is_harmonic=True,
                ...     pitch=abjad.NamedPitch("d'"),
                ...     )
                >>> abjad.attach(trill, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \once \override TrillPitchHead.stencil = #(lambda (grob) (grob-interpret-markup grob #{ \markup \musicglyph #"noteheads.s0harmonic" #}))
                    \pitchedTrill
                    c'8 \startTrillSpan d'
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

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> pitch = abjad.NamedPitch('C#4')
                >>> trill = abjad.TrillSpanner(pitch=pitch)
                >>> abjad.attach(trill, staff[:2])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \pitchedTrill c'8 \startTrillSpan cs'
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            ::

                >>> trill.pitch
                NamedPitch("cs'")

        ..  container:: example

            Returns none when trill spanner is unpitched:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> trill = abjad.TrillSpanner()
                >>> abjad.attach(trill, staff[:2])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 \startTrillSpan
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            ::

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

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> pitch = abjad.NamedPitch('C#4')
                >>> trill = abjad.TrillSpanner(pitch=pitch)
                >>> abjad.attach(trill, staff[:2])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \pitchedTrill c'8 \startTrillSpan cs'
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            ::

                >>> trill.written_pitch
                NamedPitch("cs'")

        ..  container:: example

            Returns none when trill spanner is unpitched:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> trill = abjad.TrillSpanner()
                >>> abjad.attach(trill, staff[:2])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 \startTrillSpan
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            ::

                >>> trill.written_pitch is None
                True

        Alias defined equal to `pitch` of trill spanner.

        Defaults to none.

        Property can not be set.

        Returns named pitch or none.
        '''
        return self.pitch
