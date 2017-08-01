# -*- coding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner


class OctavationSpanner(Spanner):
    r'''Octavation spanner.

    ::

        >>> import abjad

    ..  container:: example

        Spans four notes:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> spanner = abjad.OctavationSpanner(start=1)
            >>> abjad.attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \ottava #1
                c'4
                d'4
                e'4
                f'4
                \ottava #0
            }

    ..  container:: example

        Spans one note:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> octavation_spanner = abjad.OctavationSpanner(start=1)
            >>> abjad.attach(octavation_spanner, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \ottava #1
                c'4
                \ottava #0
                d'4
                e'4
                f'4
            }

        One-note octavation changes are allowed.

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        start=1,
        stop=0,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        assert isinstance(start, (int, type(None)))
        self._start = start
        assert isinstance(stop, (int, type(None)))
        self._stop = stop

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._start = self.start
        new._stop = self.stop

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_first_leaf(leaf):
            string = r'\ottava #{}'.format(self.start)
            bundle.before.commands.append(string)
        if self._is_my_last_leaf(leaf):
            string = r'\ottava #{}'.format(self.stop)
            bundle.after.commands.append(string)
        return bundle

    ### PUBLIC METHODS ###

    # TODO: add two or three more examples to better show what's going on
    def adjust_automatically(
        self,
        ottava_breakpoint=None,
        quindecisima_breakpoint=None,
        ):
        r"""Adjusts octavation spanner start and stop
        automatically according to `ottava_breakpoint`
        and `quindecisima_breakpoint`.

        ..  container:: example

            ::

                >>> measure = abjad.Measure((4, 8), "c'''8 d'''8 ef'''8 f'''8")
                >>> octavation = abjad.OctavationSpanner()
                >>> abjad.attach(octavation, measure[:])
                >>> show(measure) # doctest: +SKIP

            ::

                >>> octavation.adjust_automatically(ottava_breakpoint=14)
                >>> show(measure) # doctest: +SKIP

            ..  docs::

                >>> f(measure)
                    {
                        \time 4/8
                        \ottava #1
                        c'''8
                        d'''8
                        ef'''8
                        f'''8
                        \ottava #0
                    }

        Adjusts start and stop according to the diatonic pitch number of
        the maximum pitch in spanner.

        Returns none.
        """
        pitches = pitchtools.PitchSegment.from_selection(self)
        max_pitch = max(pitches)
        max_numbered_diatonic_pitch = max_pitch._get_diatonic_pitch_number()
        if ottava_breakpoint is not None:
            if ottava_breakpoint <= max_numbered_diatonic_pitch:
                # TODO: do not adjust in place
                #       create & attach new spanner instead
                self._start = 1
                if quindecisima_breakpoint is not None:
                    if quindecisima_breakpoint <= max_numbered_diatonic_pitch:
                        self._start = 2

    ### PUBLIC PROPERTIES ###

    @property
    def start(self):
        r'''Gets octavation start.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> spanner = abjad.OctavationSpanner(start=1)
                >>> abjad.attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> spanner.start
                1

        Returns integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets octavation stop.

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.OctavationSpanner(start=2, stop=1)
            >>> abjad.attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> spanner.stop
            1

        Returns integer or none.
        '''
        return self._stop
