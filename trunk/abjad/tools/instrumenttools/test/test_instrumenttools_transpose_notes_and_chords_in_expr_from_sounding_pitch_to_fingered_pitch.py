from abjad import *


def test_instrumenttools_transpose_notes_and_chords_in_expr_from_sounding_pitch_to_fingered_pitch_01():

    staff = Staff("<c' e' g'>4 d'4 r4 e'4")
    clarinet = instrumenttools.BFlatClarinet()(staff)
    clarinet.instrument_name_markup = 'Clarinet in B-flat'
    clarinet.short_instrument_name_markup = 'Cl. B-flat'

    for leaf in staff.leaves:
        if isinstance(leaf, (Note, Chord)):
            assert leaf.written_pitch_indication_is_at_sounding_pitch

    instrumenttools.transpose_notes_and_chords_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

    r'''
    \new Staff {
        \set Staff.instrumentName = \markup { Clarinet in B-flat }
        \set Staff.shortInstrumentName = \markup { Cl. B-flat }
        <d' fs' a'>4
        e'4
        r4
        fs'4
    }
    '''

    for leaf in staff.leaves:
        if isinstance(leaf, (Note, Chord)):
            assert not leaf.written_pitch_indication_is_at_sounding_pitch

    assert staff.format == "\\new Staff {\n\t\\set Staff.instrumentName = \\markup { Clarinet in B-flat }\n\t\\set Staff.shortInstrumentName = \\markup { Cl. B-flat }\n\t<d' fs' a'>4\n\te'4\n\tr4\n\tfs'4\n}"
