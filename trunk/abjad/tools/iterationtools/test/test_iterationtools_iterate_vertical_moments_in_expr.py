# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_vertical_moments_in_expr_01():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    piano_staff = scoretools.PianoStaff([])
    piano_staff = scoretools.PianoStaff()
    piano_staff.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = contexttools.ClefMark('bass')
    clef.attach(piano_staff[1])
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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

    moment_generator = iterationtools.iterate_vertical_moments_in_expr(
        score, reverse=True)
    moments = list(moment_generator)

    r'''
    (Note(b', 8), Note(g', 4), Note(c', 8))
    (Note(b', 8), Note(g', 4), Note(d', 8))
    (Note(c'', 8), Note(g', 4), Note(d', 8))
    (Note(c'', 8), Note(a', 4), Note(e', 8))
    (Note(d'', 8), Note(a', 4), Note(e', 8))
    (Note(d'', 8), Note(a', 4), Note(f', 8))
    '''

    tuplet = score[0][0].select_leaves()
    treble = piano_staff[0].select_leaves()
    bass = piano_staff[1].select_leaves()

    assert moments[0].leaves == (tuplet[2], treble[1], bass[3])
    assert moments[1].leaves == (tuplet[2], treble[1], bass[2])
    assert moments[2].leaves == (tuplet[1], treble[1], bass[2])
    assert moments[3].leaves == (tuplet[1], treble[0], bass[1])
    assert moments[4].leaves == (tuplet[0], treble[0], bass[1])
    assert moments[5].leaves == (tuplet[0], treble[0], bass[0])


def test_iterationtools_iterate_vertical_moments_in_expr_02():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    piano_staff = scoretools.PianoStaff([])
    piano_staff = scoretools.PianoStaff()
    piano_staff.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = contexttools.ClefMark('bass')
    clef.attach(piano_staff[1])
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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

    moment_generator = iterationtools.iterate_vertical_moments_in_expr(
        piano_staff, reverse=True)
    moments = list(moment_generator)

    r'''
    (Note(g', 4), Note(c', 8))
    (Note(g', 4), Note(d', 8))
    (Note(a', 4), Note(e', 8))
    (Note(a', 4), Note(f', 8))
    '''

    treble = piano_staff[0].select_leaves()
    bass = piano_staff[1].select_leaves()

    assert moments[0].leaves == (treble[1], bass[3])
    assert moments[1].leaves == (treble[1], bass[2])
    assert moments[2].leaves == (treble[0], bass[1])
    assert moments[3].leaves == (treble[0], bass[0])


def test_iterationtools_iterate_vertical_moments_in_expr_03():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    piano_staff = scoretools.PianoStaff([])
    piano_staff = scoretools.PianoStaff()
    piano_staff.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = contexttools.ClefMark('bass')
    clef.attach(piano_staff[1])
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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

    moment_generator = iterationtools.iterate_vertical_moments_in_expr(score)
    moments = list(moment_generator)

    r'''
    (Note(d'', 8), Note(a', 4), Note(f', 8))
    (Note(d'', 8), Note(a', 4), Note(e', 8))
    (Note(c'', 8), Note(a', 4), Note(e', 8))
    (Note(c'', 8), Note(g', 4), Note(d', 8))
    (Note(b', 8), Note(g', 4), Note(d', 8))
    (Note(b', 8), Note(g', 4), Note(c', 8))
    '''

    tuplet = score[0][0].select_leaves()
    treble = piano_staff[0].select_leaves()
    bass = piano_staff[1].select_leaves()

    assert set(moments[0].leaves) == set((tuplet[0], treble[0], bass[0]))
    assert set(moments[1].leaves) == set((tuplet[0], treble[0], bass[1]))
    assert set(moments[2].leaves) == set((tuplet[1], treble[0], bass[1]))
    assert set(moments[3].leaves) == set((tuplet[1], treble[1], bass[2]))
    assert set(moments[4].leaves) == set((tuplet[2], treble[1], bass[2]))
    assert set(moments[5].leaves) == set((tuplet[2], treble[1], bass[3]))


def test_iterationtools_iterate_vertical_moments_in_expr_04():

    score = Score([])
    staff_1 = Staff([Tuplet((4, 3), "d''8 c''8 b'8")])
    score.append(staff_1)
    piano_staff = scoretools.PianoStaff([])
    piano_staff = scoretools.PianoStaff()
    piano_staff.extend([Staff("a'4 g'4"), Staff("f'8 e'8 d'8 c'8")])
    clef = contexttools.ClefMark('bass')
    clef.attach(piano_staff[1])
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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

    moment_generator = iterationtools.iterate_vertical_moments_in_expr(
        piano_staff)
    moments = list(moment_generator)

    r'''
    (Note(a', 4), Note(f', 8))
    (Note(a', 4), Note(e', 8))
    (Note(g', 4), Note(d', 8))
    (Note(g', 4), Note(c', 8))
    '''

    treble = piano_staff[0].select_leaves()
    bass = piano_staff[1].select_leaves()

    assert set(moments[0].leaves) == set((treble[0], bass[0]))
    assert set(moments[1].leaves) == set((treble[0], bass[1]))
    assert set(moments[2].leaves) == set((treble[1], bass[2]))
    assert set(moments[3].leaves) == set((treble[1], bass[3]))
