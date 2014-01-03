# -*- encoding: utf-8 -*-
import fractions
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class TupletMonadRhythmMaker(RhythmMaker):
    r'''Tuplet monad rhythm-maker:

    ::

        >>> maker = rhythmmakertools.TupletMonadRhythmMaker()

    Initialize and then call on arbitrary divisions:

    ::

        >>> divisions = [(2, 5), (2, 5), (1, 4), (1, 5), (3, 4)]
        >>> tuplet_lists = maker(divisions)
        >>> tuplets = sequencetools.flatten_sequence(tuplet_lists)
        >>> staff = scoretools.RhythmicStaff(tuplets)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, beam_each_cell=False, beam_cells_together=False):
        RhythmMaker.__init__(self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together
            )

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls tuplet monad rhythm-maker on `divisions`.

        Returns list of tuplets.
        '''
        result = []
        for division in divisions:
            monad = self._make_monad(division)
            result.append([monad])
        return result

    def __format__(self, format_specification=''):
        r'''Formats tuplet monad rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.TupletMonadRhythmMaker(
                beam_each_cell=False,
                beam_cells_together=False,
                )

        Returns string.
        '''
        superclass = super(TupletMonadRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new tuplet monad rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker)

        ::

            >>> print format(new_maker)
            rhythmmakertools.TupletMonadRhythmMaker(
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(2, 5), (2, 5), (1, 4), (1, 5), (3, 4)]
            >>> tuplet_lists = new_maker(divisions)
            >>> tuplets = sequencetools.flatten_sequence(tuplet_lists)
            >>> staff = scoretools.RhythmicStaff(tuplets)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new tuplet monad rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_monad(self, division):
        numerator, talea_denominator = division
        power_of_two_denominator = \
            mathtools.greatest_power_of_two_less_equal(talea_denominator)
        duration = fractions.Fraction(abs(numerator), talea_denominator)
        power_of_two_duration = \
            fractions.Fraction(abs(numerator), power_of_two_denominator)
        power_of_two_division = (numerator, power_of_two_denominator)
        tuplet_multiplier = duration / power_of_two_duration
        leaves = scoretools.make_leaves([0], [power_of_two_division])
        tuplet = scoretools.Tuplet(tuplet_multiplier, leaves)
        return tuplet

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses tuplet monad rhythm-maker.

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.TupletMonadRhythmMaker(
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(2, 5), (2, 5), (1, 4), (1, 5), (3, 4)]
            >>> tuplet_lists = reversed_maker(divisions)
            >>> tuplets = sequencetools.flatten_sequence(tuplet_lists)
            >>> staff = scoretools.RhythmicStaff(tuplets)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new tuplet monad rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
