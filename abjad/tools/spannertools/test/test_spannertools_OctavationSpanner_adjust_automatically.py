import abjad


def test_spannertools_OctavationSpanner_adjust_automatically_01():

    maker = abjad.NoteMaker()
    notes = maker([24, 26, 27, 29], [(1, 8)])
    container = abjad.Container(notes)

    octavation_spanner = abjad.OctavationSpanner()
    abjad.attach(octavation_spanner, container[:])
    octavation_spanner.adjust_automatically(ottava_breakpoint=14)

    assert format(container) == abjad.String.normalize(
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

    assert abjad.inspect(container).is_well_formed()


def test_spannertools_OctavationSpanner_adjust_automatically_02():

    note = abjad.Note(31, (1, 4))
    container = abjad.Container([note])
    assert container[0].written_pitch.to_staff_position() == \
        abjad.StaffPosition(18)

    octavation_spanner = abjad.OctavationSpanner()
    abjad.attach(octavation_spanner, container[:])
    octavation_spanner.adjust_automatically(
        ottava_breakpoint=15,
        quindecisima_breakpoint=19,
        )

    assert format(container) == abjad.String.normalize(
        r"""
        {
            \ottava #1
            g'''4
            \ottava #0
        }
        """
        )

    assert abjad.inspect(container).is_well_formed()
