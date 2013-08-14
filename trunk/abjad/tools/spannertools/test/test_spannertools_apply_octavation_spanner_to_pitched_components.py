# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_apply_octavation_spanner_to_pitched_components_01():

    container = Container(notetools.make_notes([24, 26, 27, 29], [(1, 8)]))
    spannertools.apply_octavation_spanner_to_pitched_components(
        container, 
        ottava_numbered_diatonic_pitch=14,
        )

    assert testtools.compare(
        container,
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

    assert select(container).is_well_formed()


def test_spannertools_apply_octavation_spanner_to_pitched_components_02():

    container = Container([Note(31, (1, 4))])
    assert container[0].written_pitch.numbered_diatonic_pitch == 18
    spannertools.apply_octavation_spanner_to_pitched_components(
        container,
        ottava_numbered_diatonic_pitch = 15, 
        quindecisima_numbered_diatonic_pitch=19,
        )

    assert testtools.compare(
        container,
        r"""
        {
            \ottava #1
            g'''4
            \ottava #0
        }
        """
        )

    assert select(container).is_well_formed()
