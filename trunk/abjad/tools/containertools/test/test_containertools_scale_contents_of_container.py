from abjad import *


def test_containertools_scale_contents_of_container_01():
    '''Scale leaves in voice by 3/2; ie, dot leaves.'''

    t = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(3, 2))

    r'''
    \new Voice {
        c'8.
        d'8.
        e'8.
        f'8.
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8.\n\td'8.\n\te'8.\n\tf'8.\n}"


def test_containertools_scale_contents_of_container_02():
    '''Scale leaves in voice by 5/4; ie, quarter-tie leaves.'''

    t = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(5, 4))

    r'''
    \new Voice {
        c'8 ~
        c'32
        d'8 ~
        d'32
        e'8 ~
        e'32
        f'8 ~
        f'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"


def test_containertools_scale_contents_of_container_03():
    '''Scale leaves in voice by untied nonbinary 4/3; ie, tupletize notes.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(4, 3))

    r'''
    \new Voice {
        \times 2/3 {
            c'4
        }
        \times 2/3 {
            d'4
        }
        \times 2/3 {
            e'4
        }
        \times 2/3 {
            f'4
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'4\n\t}\n\t\\times 2/3 {\n\t\td'4\n\t}\n\t\\times 2/3 {\n\t\te'4\n\t}\n\t\\times 2/3 {\n\t\tf'4\n\t}\n}"


def test_containertools_scale_contents_of_container_04():
    '''Scale leaves in voice by tied nonbinary 5/4; ie, tupletize notes.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(5, 6))

    r'''
    \new Voice {
        \times 2/3 {
            c'8 ~
            c'32
        }
        \times 2/3 {
            d'8 ~
            d'32
        }
        \times 2/3 {
            e'8 ~
            e'32
        }
        \times 2/3 {
            f'8 ~
            f'32
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 ~\n\t\tc'32\n\t}\n\t\\times 2/3 {\n\t\td'8 ~\n\t\td'32\n\t}\n\t\\times 2/3 {\n\t\te'8 ~\n\t\te'32\n\t}\n\t\\times 2/3 {\n\t\tf'8 ~\n\t\tf'32\n\t}\n}"


def test_containertools_scale_contents_of_container_05():
    '''Scale mixed notes and tuplets.'''

    t = Voice([Note(0, (3, 16)),
        tuplettools.FixedDurationTuplet(Duration(3, 8), notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        c'8.
        \fraction \times 3/4 {
            d'8
            e'8
            f'8
            g'8
        }
    }
    '''

    containertools.scale_contents_of_container(t, Duration(2, 3))

    r'''
    \new Voice {
        c'8
        {
            d'16
            e'16
            f'16
            g'16
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8\n\t{\n\t\td'16\n\t\te'16\n\t\tf'16\n\t\tg'16\n\t}\n}"


def test_containertools_scale_contents_of_container_06():
    '''Undo scale of 5/4 with scale of 4/5.'''

    t = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(t, Duration(5, 4))

    r'''
    \new Voice {
        c'8 ~
        c'32
        d'8 ~
        d'32
        e'8 ~
        e'32
        f'8 ~
        f'32
    }
    '''

    assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"

    containertools.scale_contents_of_container(t, Duration(4, 5))

    r'''
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_containertools_scale_contents_of_container_07():
    '''Double all contents, including measure.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
    }
    '''

    containertools.scale_contents_of_container(t, Duration(2))

    r'''
    \new Voice {
        {
            \time 2/4
            c'4
            d'4
        }
        {
            \time 2/4
            e'4
            f'4
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\t\\time 2/4\n\t\tc'4\n\t\td'4\n\t}\n\t{\n\t\t\\time 2/4\n\t\te'4\n\t\tf'4\n\t}\n}"


def test_containertools_scale_contents_of_container_08():
    '''Multiply all contents by 5/4, including measure.'''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
    }
    '''

    containertools.scale_contents_of_container(t, Duration(5, 4))

    r'''
    \new Voice {
        {
            \time 20/64
            c'8 ~
            c'32
            d'8 ~
            d'32
        }
        {
            \time 20/64
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\t\\time 20/64\n\t\tc'8 ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32\n\t}\n\t{\n\t\t\\time 20/64\n\t\te'8 ~\n\t\te'32\n\t\tf'8 ~\n\t\tf'32\n\t}\n}"
