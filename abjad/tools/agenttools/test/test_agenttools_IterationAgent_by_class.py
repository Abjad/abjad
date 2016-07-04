# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_class_01():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")
    chords = iterate(staff).by_class(Chord)
    chords = list(chords)

    assert chords[0] is staff[0]
    assert chords[1] is staff[3]


def test_agenttools_IterationAgent_by_class_02():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")
    chords = iterate(staff).by_class(Chord, reverse=True)
    chords = list(chords)

    assert chords[0] is staff[3]
    assert chords[1] is staff[0]


def test_agenttools_IterationAgent_by_class_03():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    leaves = list(iterate(staff).by_leaf())
    beam = Beam()
    attach(beam, leaves)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    components = list(iterate(beam).by_class(reverse=True))
    leaves = list(iterate(staff).by_leaf())

    assert components[0] is leaves[-1]
    assert components[1] is leaves[-2]
    assert components[2] is leaves[-3]
    assert components[3] is leaves[-4]


def test_agenttools_IterationAgent_by_class_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    spanner = Beam()
    attach(spanner, staff[2:])
    components = iterate(spanner).by_class()
    components = list(components)

    assert components == staff[2:]


def test_agenttools_IterationAgent_by_class_05():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Multiplier(2, 3), staff[1][:])
    staff.is_simultaneous = True
    containers = iterate(staff).by_class(Container, reverse=True)
    containers = list(containers)

    assert containers[0] is staff
    assert containers[1] is staff[1]
    assert containers[2] is tuplet
    assert containers[3] is staff[0]


def test_agenttools_IterationAgent_by_class_06():

    staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
    tuplet = Tuplet(Multiplier(2, 3), staff[1][:])
    staff.is_simultaneous = True
    containers = iterate(staff).by_class(Container)
    containers = list(containers)

    assert containers[0] is staff
    assert containers[1] is staff[0]
    assert containers[2] is staff[1]
    assert containers[3] is tuplet


def test_agenttools_IterationAgent_by_class_07():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        ''',
        )

    leaves = iterate(staff).by_class(scoretools.Leaf, reverse=True)
    leaves = list(leaves)

    assert leaves[0] is staff[2][1]
    assert leaves[1] is staff[2][0]
    assert leaves[2] is staff[1][1]
    assert leaves[3] is staff[1][0]
    assert leaves[4] is staff[0][1]
    assert leaves[5] is staff[0][0]


def test_agenttools_IterationAgent_by_class_08():
    r'''Optional start and stop keyword parameters.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = iterate(staff).by_class(scoretools.Leaf, start=3, reverse=True)
    leaves = list(leaves)

    assert leaves[0] is staff[1][0]
    assert leaves[1] is staff[0][1]
    assert leaves[2] is staff[0][0]
    assert len(leaves) == 3

    leaves = iterate(staff).by_class(
        scoretools.Leaf, start=0, stop=3, reverse=True)
    leaves = list(leaves)

    assert leaves[0] is staff[2][1]
    assert leaves[1] is staff[2][0]
    assert leaves[2] is staff[1][1]
    assert len(leaves) == 3

    leaves = iterate(staff).by_class(
        scoretools.Leaf, start=2, stop=4, reverse=True)
    leaves = list(leaves)

    assert leaves[0] is staff[1][1]
    assert leaves[1] is staff[1][0]
    assert len(leaves) == 2


def test_agenttools_IterationAgent_by_class_09():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        ''',
        )

    leaves = iterate(staff).by_class(scoretools.Leaf)
    leaves = list(leaves)

    assert leaves[0] is staff[0][0]
    assert leaves[1] is staff[0][1]
    assert leaves[2] is staff[1][0]
    assert leaves[3] is staff[1][1]
    assert leaves[4] is staff[2][0]
    assert leaves[5] is staff[2][1]


def test_agenttools_IterationAgent_by_class_10():
    r'''Optional start and stop keyword parameters.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = iterate(staff).by_class(scoretools.Leaf, start=3)
    leaves = list(leaves)

    assert leaves[0] is staff[1][1]
    assert leaves[1] is staff[2][0]
    assert leaves[2] is staff[2][1]
    assert len(leaves) == 3

    leaves = iterate(staff).by_class(scoretools.Leaf, start=0, stop=3)
    leaves = list(leaves)

    assert leaves[0] is staff[0][0]
    assert leaves[1] is staff[0][1]
    assert leaves[2] is staff[1][0]
    assert len(leaves) == 3

    leaves = iterate(staff).by_class(scoretools.Leaf, start=2, stop=4)
    leaves = list(leaves)

    assert leaves[0] is staff[1][0]
    assert leaves[1] is staff[1][1]
    assert len(leaves) == 2


def test_agenttools_IterationAgent_by_class_11():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        ''',
        )

    measures = iterate(staff).by_class(Measure, reverse=True)
    measures = list(measures)

    assert measures[0] is staff[2]
    assert measures[1] is staff[1]
    assert measures[2] is staff[0]


def test_agenttools_IterationAgent_by_class_12():
    r'''Optional start and stop keyword paramters.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    measures = iterate(staff).by_class(Measure, start=1, reverse=True)
    measures = list(measures)

    assert measures[0] is staff[1]
    assert measures[1] is staff[0]
    assert len(measures) == 2

    measures = iterate(staff).by_class(Measure, stop=2, reverse=True)
    measures = list(measures)

    assert measures[0] is staff[2]
    assert measures[1] is staff[1]
    assert len(measures) == 2


def test_agenttools_IterationAgent_by_class_13():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        ''',
        )

    measures = iterate(staff).by_class(Measure)
    measures = list(measures)

    assert measures[0] is staff[0]
    assert measures[1] is staff[1]
    assert measures[2] is staff[2]


def test_agenttools_IterationAgent_by_class_14():
    r'''Optional start and stop keyword paramters.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    measures = iterate(staff).by_class(Measure, start=1)
    measures = list(measures)

    assert measures[0] is staff[1]
    assert measures[1] is staff[2]
    assert len(measures) == 2

    measures = iterate(staff).by_class(Measure, stop=2)
    measures = list(measures)

    assert measures[0] is staff[0]
    assert measures[1] is staff[1]
    assert len(measures) == 2


def test_agenttools_IterationAgent_by_class_15():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")
    notes_and_chords = iterate(staff).by_class((Note, Chord), reverse=True)
    notes_and_chords = list(notes_and_chords)

    assert len(notes_and_chords) == 3
    assert notes_and_chords[0] is staff[3]
    assert notes_and_chords[1] is staff[1]
    assert notes_and_chords[2] is staff[0]


def test_agenttools_IterationAgent_by_class_16():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")
    notes_and_chords = iterate(staff).by_class((Note, Chord))
    notes_and_chords = list(notes_and_chords)

    assert len(notes_and_chords) == 3
    assert notes_and_chords[0] is staff[0]
    assert notes_and_chords[1] is staff[1]
    assert notes_and_chords[2] is staff[3]


def test_agenttools_IterationAgent_by_class_17():

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    notes = iterate(staff).by_class(Note, reverse=True)
    notes = list(notes)

    assert notes[0] is staff[2][1]
    assert notes[1] is staff[2][0]
    assert notes[2] is staff[1][1]
    assert notes[3] is staff[1][0]
    assert notes[4] is staff[0][1]
    assert notes[5] is staff[0][0]


def test_agenttools_IterationAgent_by_class_18():
    r'''Optional start and stop keyword parameters.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    notes = iterate(staff).by_class(Note, reverse=True, start=3)
    notes = list(notes)

    assert notes[0] is staff[1][0]
    assert notes[1] is staff[0][1]
    assert notes[2] is staff[0][0]
    assert len(notes) == 3

    notes = iterate(staff).by_class(Note, reverse=True, start=0, stop=3)
    notes = list(notes)

    assert notes[0] is staff[2][1]
    assert notes[1] is staff[2][0]
    assert notes[2] is staff[1][1]
    assert len(notes) == 3

    notes = iterate(staff).by_class(Note, reverse=True, start=2, stop=4)
    notes = list(notes)

    assert notes[0] is staff[1][1]
    assert notes[1] is staff[1][0]
    assert len(notes) == 2


def test_agenttools_IterationAgent_by_class_19():

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    notes = iterate(staff).by_class(Note)
    notes = list(notes)

    assert notes[0] is staff[0][0]
    assert notes[1] is staff[0][1]
    assert notes[2] is staff[1][0]
    assert notes[3] is staff[1][1]
    assert notes[4] is staff[2][0]
    assert notes[5] is staff[2][1]


def test_agenttools_IterationAgent_by_class_20():
    r'''Optional start and stop keyword parameters.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    notes = iterate(staff).by_class(Note, start=3)
    notes = list(notes)

    assert notes[0] is staff[1][1]
    assert notes[1] is staff[2][0]
    assert notes[2] is staff[2][1]
    assert len(notes) == 3

    notes = iterate(staff).by_class(Note, start=0, stop=3)
    notes = list(notes)

    assert notes[0] is staff[0][0]
    assert notes[1] is staff[0][1]
    assert notes[2] is staff[1][0]
    assert len(notes) == 3

    notes = iterate(staff).by_class(Note, start=2, stop=4)
    notes = list(notes)

    assert notes[0] is staff[1][0]
    assert notes[1] is staff[1][1]
    assert len(notes) == 2


def test_agenttools_IterationAgent_by_class_21():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")
    rests = iterate(staff).by_class(Rest, reverse=True)
    rests = list(rests)

    assert rests[0] is staff[4]
    assert rests[1] is staff[2]


def test_agenttools_IterationAgent_by_class_22():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")
    rests = iterate(staff).by_class(Rest)
    rests = list(rests)

    assert rests[0] is staff[2]
    assert rests[1] is staff[4]


def test_agenttools_IterationAgent_by_class_23():

    score_1 = Score([Staff("c'8 d'8 e'8 f'8")])
    score_2 = Score([Staff("c'1"), Staff("g'1")])
    scores = [score_1, score_2]
    scores = iterate(scores).by_class(Score, reverse=True)
    scores = list(scores)

    assert scores[0] is score_2
    assert scores[1] is score_1


def test_agenttools_IterationAgent_by_class_24():

    score_1 = Score([Staff("c'8 d'8 e'8 f'8")])
    score_2 = Score([Staff("c'1"), Staff("g'1")])
    scores = [score_1, score_2]
    scores = iterate(scores).by_class(Score)
    scores = list(scores)

    assert scores[0] is score_1
    assert scores[1] is score_2


def test_agenttools_IterationAgent_by_class_25():

    staff = Staff("<e' g' c''>8 a'8 s8 <d' f' b'>8 s2")
    skips = iterate(staff).by_class(scoretools.Skip)
    skips = list(skips)

    assert skips[0] is staff[2]
    assert skips[1] is staff[4]


def test_agenttools_IterationAgent_by_class_26():

    staff = Staff("<e' g' c''>8 a'8 s8 <d' f' b'>8 s2")
    skips = iterate(staff).by_class(scoretools.Skip, reverse=True)
    skips = list(skips)

    assert skips[0] is staff[4]
    assert skips[1] is staff[2]


def test_agenttools_IterationAgent_by_class_27():

    score = Score(4 * Staff([]))
    score[0].name = '1'
    score[1].name = '2'
    score[2].name = '3'
    score[3].name = '4'
    staves = iterate(score).by_class(Staff, reverse=True)

    for i, staff in enumerate(staves):
        assert staff.name == str(4 - i)


def test_agenttools_IterationAgent_by_class_28():

    score = Score(4 * Staff([]))
    score[0].name = '1'
    score[1].name = '2'
    score[2].name = '3'
    score[3].name = '4'
    staves = iterate(score).by_class(Staff)

    for i, staff in enumerate(staves):
        assert staff.name == str(i + 1)


def test_agenttools_IterationAgent_by_class_29():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    tuplet_0 = Tuplet(Multiplier(2, 3), staff[:3])
    tuplet_1 = Tuplet(Multiplier(2, 3), staff[-3:])
    tuplets = iterate(staff).by_class(Tuplet, reverse=True)
    tuplets = list(tuplets)

    assert tuplets[0] is tuplet_1
    assert tuplets[1] is tuplet_0


def test_agenttools_IterationAgent_by_class_30():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    tuplet_0 = Tuplet(Multiplier(2, 3), staff[:3])
    tuplet_1 = Tuplet(Multiplier(2, 3), staff[-3:])
    tuplets = iterate(staff).by_class(Tuplet)
    tuplets = list(tuplets)

    assert tuplets[0] is tuplet_0
    assert tuplets[1] is tuplet_1


def test_agenttools_IterationAgent_by_class_31():

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'4 b4")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    voices = iterate(staff).by_class(Voice, reverse=True)
    voices = list(voices)

    assert voices[0] is voice_2
    assert voices[1] is voice_1


def test_agenttools_IterationAgent_by_class_32():

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'4 b4")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    voices = iterate(staff).by_class(Voice)
    voices = list(voices)

    assert voices[0] is voice_1
    assert voices[1] is voice_2