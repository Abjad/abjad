from abjad import *


def test_LilyPondCommandMark_format_01():
    '''AccidentalInterface.style manages LilyPond set-accidental-style.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(t)

    r'''
    \new Staff {
        #(set-accidental-style 'forget)
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\t#(set-accidental-style 'forget)\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondCommandMark_format_02():
    '''AccidentalInterface.style manages LilyPond set-accidental-style.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(t[1])

    r'''
    \new Staff {
        c'8
        #(set-accidental-style 'forget)
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\t#(set-accidental-style 'forget)\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondCommandMark_format_03():
    '''Barline after leaf.'''

    t = Note("c'4")
    marktools.LilyPondCommandMark(r'break', 'after')(t)

    r'''
    c'4
    \break
    '''

    assert t.format == 'c\'4\n\\break'


def test_LilyPondCommandMark_format_04():
    '''Barline at container closing.'''

    t = Staff()
    marktools.LilyPondCommandMark(r'break')(t)

    r'''
    \new Staff {
        \break
    }
    '''

    assert t.format == '\\new Staff {\n\t\\break\n}'


def test_LilyPondCommandMark_format_05():
    '''Add a natural harmonic.'''

    t = Note("c'4")
    marktools.LilyPondCommandMark('flageolet', 'right')(t)
    assert t.format == "c'4 \\flageolet"


def test_LilyPondCommandMark_format_06():
    '''Add and then remove natural harmonic.'''

    t = Note("c'4")
    marktools.LilyPondCommandMark('flageolet', 'right')(t)
    marktools.detach_lilypond_command_marks_attached_to_component(t, 'flageolet')
    assert t.format == "c'4"


def test_LilyPondCommandMark_format_07():

    staff = Staff([Note("c'4")])
    marktools.LilyPondCommandMark('compressFullBarRests')(staff[0])

    r'''
    \new Staff {
        \compressFullBarRests
        c'4
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\compressFullBarRests\n\tc'4\n}"


def test_LilyPondCommandMark_format_08():

    staff = Staff([Note("c'4")])
    marktools.LilyPondCommandMark('expandFullBarRests')(staff[0])

    r'''
    \new Staff {
        \expandFullBarRests
        c'4
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\expandFullBarRests\n\tc'4\n}"


def test_LilyPondCommandMark_format_09():
    '''Voice number can be set on leaves.'''

    t = Voice(notetools.make_repeated_notes(4))
    marktools.LilyPondCommandMark('voiceOne')(t[0])

    assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_LilyPondCommandMark_format_10():
    '''Voice number can be set to 1, 2, 3, 4, or None.
    Anyhing else will throw a ValueError exception.
    '''

    t = Voice(notetools.make_repeated_notes(4))
    marktools.LilyPondCommandMark('voiceOne')(t[0])
    assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

    marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceOne')
    marktools.LilyPondCommandMark('voiceTwo')(t[0])
    assert t.format == "\\new Voice {\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

    marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceTwo')
    marktools.LilyPondCommandMark('voiceThree')(t[0])
    assert t.format == "\\new Voice {\n\t\\voiceThree\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

    marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceThree')
    marktools.LilyPondCommandMark('voiceFour')(t[0])
    assert t.format == "\\new Voice {\n\t\\voiceFour\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

    marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceFour')
    assert t.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_LilyPondCommandMark_format_11():
    '''Voice number can be set on a Voice container and on one of the leaves contained in it.
    '''

    t = Voice(notetools.make_repeated_notes(4))
    marktools.LilyPondCommandMark('voiceOne')(t)
    marktools.LilyPondCommandMark('voiceTwo')(t[1])
    assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n}"
