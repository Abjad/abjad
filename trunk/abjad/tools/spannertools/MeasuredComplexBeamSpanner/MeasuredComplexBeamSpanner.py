from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from abjad.tools.spannertools.MeasuredComplexBeamSpanner._MeasuredComplexBeamSpannerFormatInterface import _MeasuredComplexBeamSpannerFormatInterface
from abjad.tools import durationtools


class MeasuredComplexBeamSpanner(ComplexBeamSpanner):
    r'''Abjad measured complex beam spanner::

        abjad> staff = Staff([Measure((2, 16), "c'16 d'16"), Measure((2, 16), "e'16 f'16")])

    ::

        abjad> spannertools.MeasuredComplexBeamSpanner(staff.leaves)
        MeasuredComplexBeamSpanner(c'16, d'16, e'16, f'16)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/16
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                d'16
            }
            {
                \time 2/16
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                e'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                f'16 ]
            }
        }

    Beam leaves in spanner explicitly.

    Group leaves by measures.

    Format top-level `span` beam between measures.

    Return measured complex beam spanner.
    '''

    def __init__(self, components = None, lone = False, span = 1, direction = None):
        ComplexBeamSpanner.__init__(self, components = components, lone = lone, direction = direction)
        self._format = _MeasuredComplexBeamSpannerFormatInterface(self)
        self.span = span

    ### PUBLIC ATTRIBUTES ###

    @apply
    def span():
        def fget(self):
            '''Get top-level beam count::

                abjad> staff = Staff([Measure((2, 16), "c'16 d'16"), Measure((2, 16), "e'16 f'16")])
                abjad> beam = spannertools.MeasuredComplexBeamSpanner(staff.leaves)
                abjad> beam.span
                1

            Set top-level beam count::

                abjad> staff = Staff([Measure((2, 16), "c'16 d'16"), Measure((2, 16), "e'16 f'16")])
                abjad> beam = spannertools.MeasuredComplexBeamSpanner(staff.leaves)
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
