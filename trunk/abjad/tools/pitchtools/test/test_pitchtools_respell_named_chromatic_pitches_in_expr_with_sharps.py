from abjad import *


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_01():
    '''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates an individual pitch.'''

    t = pitchtools.NamedChromaticPitch('df', 4)
    assert pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(t) == \
        pitchtools.NamedChromaticPitch('cs', 4)


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_02():
    '''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates the pitch of one note.'''

    t = Note(('df', 4), 4)
    pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(t)
    assert t.written_pitch == pitchtools.NamedChromaticPitch('cs', 4)


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_03():
    '''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates the pitches of all notes in a chord.'''

    t = Chord([('df', 4), ('f', 4), ('af', 4)], (1, 4))
    pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(t)
    assert t.written_pitches == (pitchtools.NamedChromaticPitch('cs', 4), pitchtools.NamedChromaticPitch('f', 4), pitchtools.NamedChromaticPitch('gs', 4))


def test_pitchtools_respell_named_chromatic_pitches_in_expr_with_sharps_04():
    '''The pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()
    helper renotates all pitches in any arbirary expression.'''

    t = Staff(notetools.make_repeated_notes(12))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(t)

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ds'8
        e'8
        f'8
        fs'8
        g'8
        gs'8
        a'8
        as'8
        b'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tds'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tgs'8\n\ta'8\n\tas'8\n\tb'8\n}"
