# -*- coding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner


class OctavationSpanner(Spanner):
    r'''Octavation spanner.

    ..  container:: example

        **Example 1.** Spans four notes:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> spanner = spannertools.OctavationSpanner(start=1)
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

        **Example 2.** Spans one note:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> octavation_spanner = spannertools.OctavationSpanner(start=1)
            >>> attach(octavation_spanner, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

    def _format_after_leaf(self, leaf):
        result = []
        result.extend(Spanner._format_after_leaf(self, leaf))
        if self._is_my_last_leaf(leaf):
            string = r'\ottava #{}'.format(self.stop)
            result.append(string)
        return result

    def _format_before_leaf(self, leaf):
        result = []
        result.extend(Spanner._format_before_leaf(self, leaf))
        if self._is_my_first_leaf(leaf):
            string = r'\ottava #{}'.format(self.start)
            result.append(string)
        return result

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

                >>> measure = Measure((4, 8), "c'''8 d'''8 ef'''8 f'''8")
                >>> octavation = spannertools.OctavationSpanner()
                >>> attach(octavation, measure[:])
                >>> show(measure) # doctest: +SKIP

            ::

                >>> octavation.adjust_automatically(ottava_breakpoint=14)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
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
        max_numbered_diatonic_pitch = max_pitch.diatonic_pitch_number
        if ottava_breakpoint is not None:
            if ottava_breakpoint <= max_numbered_diatonic_pitch:
                # TODO: do not adjust in place
                #       create & attach new spanner instead
                self._start = 1
                if quindecisima_breakpoint is not None:
                    if quindecisima_breakpoint <= \
                        max_numbered_diatonic_pitch:
                        self._start = 2

    ### PUBLIC PROPERTIES ###

    @property
    def start(self):
        r'''Gets octavation start.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.OctavationSpanner(start=1)
                >>> attach(spanner, staff[:])
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

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.OctavationSpanner(start=2, stop=1)
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> spanner.stop
            1

        Returns integer or none.
        '''
        return self._stop
