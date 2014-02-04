# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner


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

    def _format_before_leaf(self, leaf):
        result = []
        if self.pitch is not None:
            if self._is_my_first_leaf(leaf):
                result.append(r'\pitchedTrill')
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\startTrillSpan')
            if self.pitch is not None:
                result.append(str(self.pitch))
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopTrillSpan')
        return result

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
