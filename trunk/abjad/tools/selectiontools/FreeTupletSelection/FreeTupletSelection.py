# -*- encoding: utf-8 -*-
import fractions
import math
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.selectiontools.Selection import Selection


class FreeTupletSelection(Selection):
    r'''A free selection of tuplets.
    '''

    ### PUBLIC METHODS ###

    def set_denominator_to_at_least(self, n):
        r'''Set denominator of tuplets in selection to at least `n`.

        ..  container:: example

            **Example.** Set denominator of tuplets to at least ``8``:

            ::

                >>> tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")

            ..  doctest::

                >>> f(tuplet)
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

            ::

                >>> show(tuplet) # doctest: +SKIP

            ::

                >>> tuplets = selectiontools.select_tuplets(tuplet)
                >>> tuplets.set_denominator_to_at_least(8)

            ..  doctest::

                >>> f(tuplet)
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 6/10 {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

            ::

                >>> show(tuplet) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import tuplettools

        assert mathtools.is_nonnegative_integer_power_of_two(n)
        Duration = durationtools.Duration
        #for tuplet in iterationtools.iterate_tuplets_in_expr(expr):
        for tuplet in self:
            tuplet.force_fraction = True
            durations = [
                tuplet._contents_duration, 
                tuplet._preprolated_duration, 
                (1, n),
                ]
            duration_pairs = Duration.durations_to_nonreduced_fractions_with_common_denominator(
                durations)
            tuplet.preferred_denominator = duration_pairs[1].numerator
