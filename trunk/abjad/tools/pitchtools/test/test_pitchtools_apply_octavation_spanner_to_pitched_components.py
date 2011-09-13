from abjad import *


def test_pitchtools_apply_octavation_spanner_to_pitched_components_01():

    t = Staff(notetools.make_notes([24, 26, 27, 29], [(1, 8)]))
    pitchtools.apply_octavation_spanner_to_pitched_components(t, ottava_numbered_diatonic_pitch = 14)

    r"""\new Staff {
        \ottava #1
        c'''8
        d'''8
        ef'''8
        f'''8
        \ottava #0
    }"""

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'''8\n\td'''8\n\tef'''8\n\tf'''8\n\t\\ottava #0\n}"


def test_pitchtools_apply_octavation_spanner_to_pitched_components_02():

    t = Voice([Note(31, (1, 4))])
    assert t[0].written_pitch.numbered_diatonic_pitch == 18
    pitchtools.apply_octavation_spanner_to_pitched_components(t,
        ottava_numbered_diatonic_pitch = 15, quindecisima_numbered_diatonic_pitch = 19)

    r"""
    \new Voice {
        \ottava #1
        g'''4
        \ottava #0
    }
    """

    assert t.format == "\\new Voice {\n\t\\ottava #1\n\tg'''4\n\t\\ottava #0\n}"
