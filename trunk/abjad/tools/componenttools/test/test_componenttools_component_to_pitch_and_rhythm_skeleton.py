from abjad import *
import py.test


def test_componenttools_component_to_pitch_and_rhythm_skeleton_01():
    '''Pitch and rhythm skeleton preserves pitch, written duration and multiplier.
    '''

    note = Note("c'4")
    note.duration_multiplier = Fraction(1, 2)
    skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(note)
    assert skeleton == "Note(('c', 4), Duration(1, 4), Fraction(1, 2))"
    new_note = eval(skeleton)
    assert new_note.format == note.format

    rest = Rest((1, 4))
    skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(rest)
    assert skeleton == "Rest(Duration(1, 4))"

    chord = Chord([0, 2, 4], (1, 4))
    skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(chord)
    assert skeleton == "Chord((('c', 4), ('d', 4), ('e', 4)), Duration(1, 4))"

    skip = skiptools.Skip((1, 4))
    skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(skip)
    assert skeleton == "Skip(Duration(1, 4))"


def test_componenttools_component_to_pitch_and_rhythm_skeleton_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(staff)

    r'''
    Staff([
        Note(('c', 4), Duration(1, 8)),
        Note(('d', 4), Duration(1, 8)),
        Note(('e', 4), Duration(1, 8)),
        Note(('f', 4), Duration(1, 8))
    ])
    '''

    assert skeleton == "Staff([\n\tNote(('c', 4), Duration(1, 8)),\n\tNote(('d', 4), Duration(1, 8)),\n\tNote(('e', 4), Duration(1, 8)),\n\tNote(('f', 4), Duration(1, 8))\n])"

    new = eval(skeleton)

    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_componenttools_component_to_pitch_and_rhythm_skeleton_03():

    tuplet = tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8 e'8 f'8")
    measure = Measure((6, 16), [tuplet])
    staff = Staff([measure])
    score = Score(staff * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

    r'''
    \new Score <<
        \new Staff {
            {
                \time 6/16
                \fraction \times 3/4 {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            }
        }
        \new Staff {
            {
                \time 6/16
                \fraction \times 3/4 {
                    g'8
                    a'8
                    b'8
                    c''8
                }
            }
        }
    >>
    '''

    skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(score)

    r'''
    Score([
        Staff([
            Measure((6, 16), [
                FixedDurationTuplet(Duration(3, 8), [
                    Note(('c', 4), Duration(1, 8)),
                    Note(('d', 4), Duration(1, 8)),
                    Note(('e', 4), Duration(1, 8)),
                    Note(('f', 4), Duration(1, 8))
                ])
            ])
        ]),
        Staff([
            Measure((6, 16), [
                FixedDurationTuplet(Duration(3, 8), [
                    Note(('g', 4), Duration(1, 8)),
                    Note(('a', 4), Duration(1, 8)),
                    Note(('b', 4), Duration(1, 8)),
                    Note(('c', 5), Duration(1, 8))
                ])
            ])
        ])
    ])
    '''

    assert skeleton == "Score([\n\tStaff([\n\t\tMeasure((6, 16), [\n\t\t\tFixedDurationTuplet(Duration(3, 8), [\n\t\t\t\tNote(('c', 4), Duration(1, 8)),\n\t\t\t\tNote(('d', 4), Duration(1, 8)),\n\t\t\t\tNote(('e', 4), Duration(1, 8)),\n\t\t\t\tNote(('f', 4), Duration(1, 8))\n\t\t\t])\n\t\t])\n\t]),\n\tStaff([\n\t\tMeasure((6, 16), [\n\t\t\tFixedDurationTuplet(Duration(3, 8), [\n\t\t\t\tNote(('g', 4), Duration(1, 8)),\n\t\t\t\tNote(('a', 4), Duration(1, 8)),\n\t\t\t\tNote(('b', 4), Duration(1, 8)),\n\t\t\t\tNote(('c', 5), Duration(1, 8))\n\t\t\t])\n\t\t])\n\t])\n])"

    from abjad.tools.tuplettools import FixedDurationTuplet
    new = eval(skeleton)

    assert componenttools.is_well_formed_component(new)
    assert new.format == "\\new Score <<\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 6/16\n\t\t\t\\fraction \\times 3/4 {\n\t\t\t\tc'8\n\t\t\t\td'8\n\t\t\t\te'8\n\t\t\t\tf'8\n\t\t\t}\n\t\t}\n\t}\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 6/16\n\t\t\t\\fraction \\times 3/4 {\n\t\t\t\tg'8\n\t\t\t\ta'8\n\t\t\t\tb'8\n\t\t\t\tc''8\n\t\t\t}\n\t\t}\n\t}\n>>"
