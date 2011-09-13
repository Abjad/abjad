from abjad import *
import py.test


def test_contexttools_get_effective_clef_01():
    '''Clef defaults to none.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in t:
        assert contexttools.get_effective_clef(note) is None


def test_contexttools_get_effective_clef_02():
    '''Clefs carry over to notes following.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(t)
    for note in t:
        assert contexttools.get_effective_clef(note) == contexttools.ClefMark('treble')


def test_contexttools_get_effective_clef_03():
    '''Clef defaults to none.
    Clefs carry over to notes following.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('bass')(t[4])
    for i, note in enumerate(t):
        if i in (0, 1, 2, 3):
            assert contexttools.get_effective_clef(note) is None
        else:
            assert contexttools.get_effective_clef(note) == contexttools.ClefMark('bass')


def test_contexttools_get_effective_clef_04():
    '''Clefs carry over to notes following.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    assert [contexttools.get_effective_clef(note) for note in t] == \
        [contexttools.ClefMark(name) for name in ['treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass']]


def test_contexttools_get_effective_clef_05():
    '''None cancels an explicit clef.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    clef = contexttools.get_effective_clef(t[4])
    clef.detach()
    for note in t:
        assert contexttools.get_effective_clef(note) == contexttools.ClefMark('treble')


def test_contexttools_get_effective_clef_06():
    '''Redudant clefs are allowed.'''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('treble')(t[4])

    r'''
    Staff {
        \clef "treble"
        c'8
        cs'8
        d'8
        ef'8
        \clef "treble"
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "treble"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}'''


def test_contexttools_get_effective_clef_07():
    '''Clefs with transposition are allowed and work as expected.'''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    contexttools.ClefMark('treble_8')(t[0])
    contexttools.ClefMark('treble')(t[4])

    r'''
    \new Staff {
        \clef "treble_8"
        c'8
        cs'8
        d'8
        ef'8
        \clef "treble"
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff {\n\t\\clef "treble_8"\n\tc\'8\n\tcs\'8\n\td\'8\n\tef\'8\n\t\\clef "treble"\n\te\'8\n\tf\'8\n\tfs\'8\n\tg\'8\n}'


def test_contexttools_get_effective_clef_08():
    '''Setting and then clearing works as expected.'''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('alto')(t[0])
    clef = contexttools.get_effective_clef(t[0])
    clef.detach()

    for leaf in t:
        assert contexttools.get_effective_clef(leaf) is None
