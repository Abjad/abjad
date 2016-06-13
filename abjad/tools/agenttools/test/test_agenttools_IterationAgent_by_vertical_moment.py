# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_vertical_moment_01():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    staff_group = StaffGroup(context_name='PianoStaff')
    staff_group.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = Clef('bass')
    attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>
        '''
        )

    moment_generator = iterate(score).by_vertical_moment(reverse=True)
    moments = list(moment_generator)

    r'''
    (Note(b', 8), Note(g', 4), Note(c', 8))
    (Note(b', 8), Note(g', 4), Note(d', 8))
    (Note(c'', 8), Note(g', 4), Note(d', 8))
    (Note(c'', 8), Note(a', 4), Note(e', 8))
    (Note(d'', 8), Note(a', 4), Note(e', 8))
    (Note(d'', 8), Note(a', 4), Note(f', 8))
    '''

    tuplet = list(iterate(score[0][0]).by_leaf())
    treble = list(iterate(staff_group[0]).by_leaf())
    bass = list(iterate(staff_group[1]).by_leaf())

    assert moments[0].leaves == (tuplet[2], treble[1], bass[3])
    assert moments[1].leaves == (tuplet[2], treble[1], bass[2])
    assert moments[2].leaves == (tuplet[1], treble[1], bass[2])
    assert moments[3].leaves == (tuplet[1], treble[0], bass[1])
    assert moments[4].leaves == (tuplet[0], treble[0], bass[1])
    assert moments[5].leaves == (tuplet[0], treble[0], bass[0])


def test_agenttools_IterationAgent_by_vertical_moment_02():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    staff_group = StaffGroup(context_name='PianoStaff')
    staff_group.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = Clef('bass')
    attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>
        '''
        )

    # see above for formatted score #

    moment_generator = iterate(staff_group).by_vertical_moment(reverse=True)
    moments = list(moment_generator)

    r'''
    (Note(g', 4), Note(c', 8))
    (Note(g', 4), Note(d', 8))
    (Note(a', 4), Note(e', 8))
    (Note(a', 4), Note(f', 8))
    '''

    treble = list(iterate(staff_group[0]).by_leaf())
    bass = list(iterate(staff_group[1]).by_leaf())

    assert moments[0].leaves == (treble[1], bass[3])
    assert moments[1].leaves == (treble[1], bass[2])
    assert moments[2].leaves == (treble[0], bass[1])
    assert moments[3].leaves == (treble[0], bass[0])


def test_agenttools_IterationAgent_by_vertical_moment_03():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    staff_group = StaffGroup(context_name='PianoStaff')
    staff_group.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = Clef('bass')
    attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>
        '''
        )

    moment_generator = iterate(score).by_vertical_moment()
    moments = list(moment_generator)

    r'''
    (Note(d'', 8), Note(a', 4), Note(f', 8))
    (Note(d'', 8), Note(a', 4), Note(e', 8))
    (Note(c'', 8), Note(a', 4), Note(e', 8))
    (Note(c'', 8), Note(g', 4), Note(d', 8))
    (Note(b', 8), Note(g', 4), Note(d', 8))
    (Note(b', 8), Note(g', 4), Note(c', 8))
    '''

    tuplet = list(iterate(score[0][0]).by_leaf())
    treble = list(iterate(staff_group[0]).by_leaf())
    bass = list(iterate(staff_group[1]).by_leaf())

    assert set(moments[0].leaves) == set((tuplet[0], treble[0], bass[0]))
    assert set(moments[1].leaves) == set((tuplet[0], treble[0], bass[1]))
    assert set(moments[2].leaves) == set((tuplet[1], treble[0], bass[1]))
    assert set(moments[3].leaves) == set((tuplet[1], treble[1], bass[2]))
    assert set(moments[4].leaves) == set((tuplet[2], treble[1], bass[2]))
    assert set(moments[5].leaves) == set((tuplet[2], treble[1], bass[3]))


def test_agenttools_IterationAgent_by_vertical_moment_04():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    staff_group = StaffGroup(context_name='PianoStaff')
    staff_group.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = Clef('bass')
    attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>
        '''
        )

    moment_generator = iterate(staff_group).by_vertical_moment()
    moments = list(moment_generator)

    r'''
    (Note(a', 4), Note(f', 8))
    (Note(a', 4), Note(e', 8))
    (Note(g', 4), Note(d', 8))
    (Note(g', 4), Note(c', 8))
    '''

    treble = list(iterate(staff_group[0]).by_leaf())
    bass = list(iterate(staff_group[1]).by_leaf())

    assert set(moments[0].leaves) == set((treble[0], bass[0]))
    assert set(moments[1].leaves) == set((treble[0], bass[1]))
    assert set(moments[2].leaves) == set((treble[1], bass[2]))
    assert set(moments[3].leaves) == set((treble[1], bass[3]))