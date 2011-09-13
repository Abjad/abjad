from abjad import *


def test_Annotation___call___01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = marktools.Annotation('foo')(staff[0])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert annotation.start_component is staff[0]
