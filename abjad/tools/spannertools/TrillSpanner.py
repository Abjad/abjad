# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class TrillSpanner(Spanner):
    r'''A trill spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> trill = spannertools.TrillSpanner()
            >>> attach(trill, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                c'8 \startTrillSpan
                d'8
                e'8
                f'8 \stopTrillSpan
            }

    Formats LilyPond ``\startTrillSpan`` on first leaf in spanner.

    Formats LilyPond ``\stopTrillSpan`` on last leaf in spanner.
    '''
    
    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        overrides=None,
        pitch=None,
        ):
        Spanner.__init__(
            self, 
            overrides=overrides,
            )
        if pitch is not None:
            pitch = pitchtools.NamedPitch(pitch)
        self._pitch = pitch

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._pitch = self.pitch

    def _get_lilypond_format_bundle(self, leaf):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        if self._is_my_first_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            lilypond_format_bundle.grob_overrides.extend(contributions)
            string = r'\startTrillSpan'
            lilypond_format_bundle.right.spanner_starts.append(string)
            if self.pitch is not None:
                string = r'\pitchedTrill'
                lilypond_format_bundle.opening.spanners.append(string)
                string = str(self.pitch)
                lilypond_format_bundle.right.spanner_starts.append(string)
        if self._is_my_last_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            lilypond_format_bundle.grob_reverts.extend(contributions)
            string = r'\stopTrillSpan'
            lilypond_format_bundle.right.spanner_stops.append(string)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def pitch(self):
        r'''Gets optional pitch of trill spanner.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> pitch = NamedPitch('C#4')
                >>> trill = spannertools.TrillSpanner(pitch=pitch)
                >>> attach(trill, staff[:2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    \pitchedTrill c'8 \startTrillSpan cs'
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            ::

                >>> trill.pitch
                NamedPitch("cs'")

        Formats LilyPond ``\pitchedTrill`` command on first leaf in spanner.

        Returns named pitch or none.
        '''
        return self._pitch

    @property
    def written_pitch(self):
        r'''Gets written pitch of trill spanner.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> pitch = NamedPitch('C#4')
                >>> trill = spannertools.TrillSpanner(pitch=pitch)
                >>> attach(trill, staff[:2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    \pitchedTrill c'8 \startTrillSpan cs'
                    d'8 \stopTrillSpan
                    e'8
                    f'8
                }

            ::

                >>> trill.written_pitch
                NamedPitch("cs'")

        Defined equal to `pitch`.

        Returns named pitch or none.
        '''
        return self.pitch
