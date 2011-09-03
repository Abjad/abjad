from abjad import *
from abjad.tools import iotools


def test_iotools_parse_lilypond_input_string_01():

    note_entry_string = r'''g'4 a'4 ~ a'2 \bar "||" g'4. fs'8 e'4 d'4 \fermata'''
    container = iotools.parse_lilypond_input_string(note_entry_string)
    staff = Staff([])
    staff[:] = container[:]

    r'''
    \new Staff {
        g'4
        a'4 ~
        a'2
        \bar "||"
        g'4.
        fs'8
        e'4
        d'4 -\fermata
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\tg\'4\n\ta\'4 ~\n\ta\'2\n\t\\bar "||"\n\tg\'4.\n\tfs\'8\n\te\'4\n\td\'4 -\\fermata\n}'


def test_iotools_parse_lilypond_input_string_02():
    '''Should handle beams chords, slurs and common lilypond articulation strings.'''

    note_entry_string = r'''c'4 g'4 b8 c'8 d'8 -. ( ef'8 ^\marcato <bf cs' f'>4 c'4 )'''
    container = iotools.parse_lilypond_input_string(note_entry_string)
    staff = Staff([])
    staff[:] = container[:]

    r'''
    \new Staff {
        c'4
        g'4
        b8
        c'8
        d'8 -\staccato (
        ef'8 ^\marcato
        <bf cs' f'>4
        c'4 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'4\n\tg'4\n\tb8\n\tc'8\n\td'8 -\\staccato (\n\tef'8 ^\\marcato\n\t<bf cs' f'>4\n\tc'4 )\n}"


def test_iotools_parse_lilypond_input_string_03():
    '''Should handle simple beams.'''

    note_entry_string = r'''c'4 ( d'4 e'8 fs'8 [ a'16. d'32 ] ) g'2 b16 [ ] ( c'16 b16 c'16 )'''
    container = iotools.parse_lilypond_input_string(note_entry_string)
    staff = Staff([])
    staff[:] = container[:]

    r'''
    \new Staff {
        c'4 (
        d'4
        e'8
        fs'8 [
        a'16.
        d'32 ] )
        g'2
        b16 [ ] (
        c'16
        b16
        c'16 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'4 (\n\td'4\n\te'8\n\tfs'8 [\n\ta'16.\n\td'32 ] )\n\tg'2\n\tb16 [ ] (\n\tc'16\n\tb16\n\tc'16 )\n}"
