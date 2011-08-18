from abjad import *


def test_Container_grob_override_01():
    '''Noncontext containers bracket grob overrides at opening and closing.'''

    t = Container("c'8 d'8 e'8 f'8")
    t.override.glissando.thickness = 3

    r'''
    {
        \override Glissando #'thickness = #3
        c'8
        d'8
        e'8
        f'8
        \revert Glissando #'thickness
    }
    '''

    assert t.format == "{\n\t\\override Glissando #'thickness = #3\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Glissando #'thickness\n}"
