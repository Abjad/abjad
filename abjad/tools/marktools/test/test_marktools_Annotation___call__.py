# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Annotation___call___01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = marktools.Annotation('foo')
    attach(annotation, staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
