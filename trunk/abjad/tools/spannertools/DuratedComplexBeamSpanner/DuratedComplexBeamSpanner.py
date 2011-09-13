from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from abjad.tools.spannertools.DuratedComplexBeamSpanner._DuratedComplexBeamSpannerFormatInterface import _DuratedComplexBeamSpannerFormatInterface
from abjad.tools import durationtools


class DuratedComplexBeamSpanner(ComplexBeamSpanner):
    r'''Abjad durated complex beam spanner::

        staff = Staff("c'16 d'16 e'16 f'16")

    ::

        durations = [Duration(1, 8), Duration(1, 8)]
        beam = spannertools.DuratedComplexBeamSpanner(staff[:], durations, 1)

    ::

        f(staff)
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            d'16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            e'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 ]
        }

    Beam all beamable leaves in spanner explicitly.

    Group leaves in spanner according to `durations`.

    Span leaves between duration groups according to `span`.

    Return durated complex beam spanner.
    '''

    def __init__(self, components = None, durations = None, span = 1, lone = False):
        ComplexBeamSpanner.__init__(self, components = components)
        self._format = _DuratedComplexBeamSpannerFormatInterface(self)
        self.durations = durations
        self.lone = lone
        self.span = span

    ### PRIVATE ATTRIBUTES ###

    @property
    def _span_points(self):
        result = []
        if self.durations is not None:
            result.append(self.durations[0])
            for d in self.durations[1:]:
                result.append(result[-1] + d)
        return result

    ### PUBLIC ATTRIBUTES ###

    @apply
    def durations():
        def fget(self):
            '''Get spanner leaf group durations::

                abjad> staff = Staff("c'16 d'16 e'16 f'16")
                abjad> durations = [Duration(1, 8), Duration(1, 8)]
                abjad> beam = spannertools.DuratedComplexBeamSpanner(staff[:], durations)
                abjad> beam.durations
                [Duration(1, 8), Duration(1, 8)]

            Set spanner leaf group durations::

                abjad> staff = Staff("c'16 d'16 e'16 f'16")
                abjad> durations = [Duration(1, 8), Duration(1, 8)]
                abjad> beam = spannertools.DuratedComplexBeamSpanner(staff[:], durations)
                abjad> beam.durations = [Duration(1, 4)]
                abjad> beam.durations
                [Duration(1, 4)]

            Set iterable.
            '''
            return self._durations
        def fset(self, arg):
            if arg is None:
                self._durations = None
            elif isinstance(arg, list):
                for i, d in enumerate(arg):
                    if isinstance(d, tuple):
                        arg[i] = durationtools.Duration(*d)
                    else:
                        arg[i] = durationtools.Duration(d)
                self._durations = arg
            else:
                raise ValueError('durations must be list of Durations, or None.')
        return property(**locals())

    @apply
    def span():
        def fget(self):
            r'''Get top-level beam count::

                abjad> staff = Staff("c'16 d'16 e'16 f'16")
                abjad> durations = [Duration(1, 8), Duration(1, 8)]
                abjad> beam = spannertools.DuratedComplexBeamSpanner(staff[:], durations, 1)
                abjad> beam.span
                1

            Set top-level beam count::

                abjad> staff = Staff("c'16 d'16 e'16 f'16")
                abjad> durations = [Duration(1, 8), Duration(1, 8)]
                abjad> beam = spannertools.DuratedComplexBeamSpanner(staff[:], durations, 1)
                abjad> beam.span = 2
                abjad> beam.span
                2

            Set nonnegative integer.
            '''
            return self._span
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._span = arg
        return property(**locals())
