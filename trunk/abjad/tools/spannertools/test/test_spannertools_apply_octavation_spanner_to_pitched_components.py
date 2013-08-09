# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_apply_octavation_spanner_to_pitched_components_01():

    staff = Staff(notetools.make_notes([24, 26, 27, 29], [(1, 8)]))
    spannertools.apply_octavation_spanner_to_pitched_components(staff, ottava_numbered_diatonic_pitch=14)

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r"""
        \new Staff {
            \ottava #1
            c'''8
            d'''8
            ef'''8
            f'''8
            \ottava #0
        }
        """
        )


def test_spannertools_apply_octavation_spanner_to_pitched_components_02():

    voice = Voice([Note(31, (1, 4))])
    assert voice[0].written_pitch.numbered_diatonic_pitch == 18
    spannertools.apply_octavation_spanner_to_pitched_components(voice,
        ottava_numbered_diatonic_pitch = 15, quindecisima_numbered_diatonic_pitch=19)

    assert testtools.compare(
        voice,
        r"""
        \new Voice {
            \ottava #1
            g'''4
            \ottava #0
        }
        """
        )
