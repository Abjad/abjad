# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner


class OctavationSpanner(Spanner):
    r'''An octavation spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> show(staff) # doctest: +SKIP


        ::

            >>> spanner = spannertools.OctavationSpanner(start=1)
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \ottava #1
                c'8
                d'8
                e'8
                f'8
                \ottava #0
            }

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None, 
        start=1, 
        stop=0,
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )
        self.start = start
        self.stop = stop

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.start = self.start
        new.stop = self.stop

    def _format_after_leaf(self, leaf):
        result = []
        result.extend(Spanner._format_after_leaf(self, leaf))
        if self._is_my_last_leaf(leaf):
            result.append(r'\ottava #%s' % self.stop)
        return result

    def _format_before_leaf(self, leaf):
        result = []
        result.extend(Spanner._format_before_leaf(self, leaf))
        if self._is_my_first_leaf(leaf):
            result.append(r'\ottava #%s' % self.start)
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def start():
        def fget(self):
            r'''Get octavation start:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.OctavationSpanner(start=1)
                >>> attach(spanner, staff[:])
                >>> spanner.start
                1

            Set octavation start:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.OctavationSpanner(start=1)
                >>> attach(spanner, staff[:])
                >>> spanner.start
                1

            Set integer.
            '''
            return self._start
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._start = arg
        return property(**locals())

    @apply
    def stop():
        def fget(self):
            r'''Get octavation stop:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.OctavationSpanner(start=2, stop=1)
                >>> attach(spanner, staff[:])
                >>> spanner.stop
                1

            Set octavation stop:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.OctavationSpanner(start=2, stop=1)
                >>> attach(spanner, staff[:])
                >>> spanner.stop = 0
                >>> spanner.stop
                0

            Set integer.
            '''
            return self._stop
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._stop = arg
        return property(**locals())

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
        max_numbered_diatonic_pitch = max_pitch.diatonic_pitch_number
        if ottava_breakpoint is not None:
            if ottava_breakpoint <= max_numbered_diatonic_pitch:
                self.start = 1
                if quindecisima_breakpoint is not None:
                    if quindecisima_breakpoint <= \
                        max_numbered_diatonic_pitch:
                        self.start = 2
