# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_OctavationSpanner_adjust_automatically_01():

    container = Container(scoretools.make_notes([24, 26, 27, 29], [(1, 8)]))

    octavation_spanner = spannertools.OctavationSpanner()
    attach(octavation_spanner, container[:])
    octavation_spanner.adjust_automatically(ottava_breakpoint=14)

    assert format(container) == stringtools.normalize(
        r"""
        {
            \ottava #1
            c'''8
            d'''8
            ef'''8
            f'''8
            \ottava #0
        }
        """
        )

    assert inspect_(container).is_well_formed()


def test_spannertools_OctavationSpanner_adjust_automatically_02():

    container = Container([Note(31, (1, 4))])
    assert container[0].written_pitch.diatonic_pitch_number == 18

    octavation_spanner = spannertools.OctavationSpanner()
    attach(octavation_spanner, container[:])
    octavation_spanner.adjust_automatically(
        ottava_breakpoint=15,
        quindecisima_breakpoint=19,
        )

    assert format(container) == stringtools.normalize(
        r"""
        {
            \ottava #1
            g'''4
            \ottava #0
        }
        """
        )

    assert inspect_(container).is_well_formed()
